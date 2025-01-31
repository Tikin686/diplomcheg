import random
import string

from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserManagerForm, UserRegisterForm
from users.models import User


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    """
    Регистрация нового пользователя.
    """

    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирование профиля пользователя.
    """

    model = User
    form_class = UserManagerForm
    success_url = reverse_lazy("users:user_list")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        """
        Переопределяем форму валидации.
        """
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("users:user_detail.html", args=[self.kwargs.get("pk")])


class UserDetailView(LoginRequiredMixin, DetailView):
    """
    Показывает детальную информацию о пользователе.
    """

    model = User
    template_name = "users/user_detail.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["note_text"] = self.object.reserves.all()
        return context

    def post(self, request, *args, **kwargs):
        note_text = request.POST.get("note_text")
        user = self.request.user
        user.notes = note_text
        user.save()
        return HttpResponseRedirect(reverse("users:user_detail.html"))


class CustomLoginView(LoginView):
    """
    Выводит форму авторизации с логином и паролем.
    """

    template_name = "users/login.html"
    success_url = reverse_lazy("restaurants:restaurant_list")

    def get_success_url(self):
        return reverse_lazy("restaurants:restaurant_list")


def generate_random_password(length=8):
    # Фун-ция кот.генерирует пароль

    # Определяем возможные символы для пароля
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ""  # Создаем пустую строку для пароля
    # Генерируем пароль
    for i in range(length):
        random_char = random.choice(characters)  # Выбираем случайный символ
        password += random_char  # Добавляем его к паролю

    return password


def reset_password(request):
    # ф-ция восстановления, пароля зарегистрированного пользователя

    if request.method == "POST":  # Мы проверяем, является ли метод запроса POST.
        email = request.POST.get("email")  # извлекаем email из запроса

        try:
            user = User.objects.get(
                email=email
            )  # пытаемся получить пользователя по email
            new_password = (
                generate_random_password()
            )  # Генерация нового пароля через ф-цию
            user.password = make_password(new_password)  # Хеширование пароля
            user.save()

            # Отправка нового пароля на электронную почту
            send_mail(
                subject="Ваш новый пароль",
                message=f"Ваш новый пароль: {new_password}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
            # Перенаправление на страницу входа после успешного восстановления
            return redirect("users:login")

        # Обработка случая, когда пользователь не найден
        except User.DoesNotExist:
            return render(
                request,
                "users/password_reset.html",
                {"error": "Пользователь с таким email не найден."},
            )
    # Если метод запроса не POST, а GET мы просто отображаем форму для восстановления пароля.
    return render(request, "users/password_reset.html")

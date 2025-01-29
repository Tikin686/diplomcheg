from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserManagerForm
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
        return reverse('users:user_detail.html', args=[self.kwargs.get('pk')])
    
    
class UserDetailView(LoginRequiredMixin, DetailView):
    """
    Показывает детальную информацию о пользователе.
    """
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['note_text'] = self.object.reserves.all()
        return context
    
    def post(self, request, *args, **kwargs):
        note_text = request.POST.get('note_text')
        user = self.request.user
        user.notes = note_text
        user.save()
        return HttpResponseRedirect(reverse('users:user_detail.html'))


class CustomLoginView(LoginView):
    """
    Выводит форму авторизации с логином и паролем.
    """
    template_name = "users/login.html"
    success_url = reverse_lazy('restaurants:restaurant_list')

    def get_success_url(self):
        return reverse_lazy('restaurants:restaurant_list')


class CustomPasswordResetView(PasswordResetView):
    """
    Выводит форму сброса пароля.
    """
    template_name = "users/password_reset.html"
    success_url = reverse_lazy('users:password_reset_done')
    email_template_name = 'users/password_reset_email.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return super().form_invalid(form)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = self.request.build_absolute_uri(reverse('users:password_reset_confirm', args=[uid, token]))

        subject = 'Сброс пароля'
        message = render_to_string('users/password_reset_email.html', {
            'user': user,
            'reset_link': reset_link
        })

        send_mail(
            subject,
            strip_tags(message),
            EMAIL_HOST_USER,
            [user.email],
            html_message=message,
        )

        return HttpResponseRedirect(self.get_success_url())
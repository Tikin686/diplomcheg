from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from restaurants.forms import (FeedbackForm, ReserveForm, ReserveUpdateForm,
                               RestaurantForm, SuperUserRequiredMixin)
from restaurants.models import Reserve, Restaurant, Table


class ReserveCancelView(LoginRequiredMixin, View):
    """
    Отмена бронирования.
    """

    def get(self, request, pk):
        reserve = get_object_or_404(Reserve, pk=pk, client=request.user)
        if reserve.is_active:
            reserve.is_active = False
            reserve.save()
            messages.success(request, "Бронирование успешно отменено.")
        else:
            messages.warning(request, "Это бронирование уже отменено.")
        return redirect("restaurants:reserve_list")


class RestaurantListView(ListView):
    """
    Список ресторанов.
    """

    model = Restaurant
    template_name = "restaurant_list.html"

    def get_queryset(self):
        """
        Возвращает список ресторанов без возможности редактирования.
        """
        return Restaurant.objects.all()


class RestaurantCreateView(CreateView):
    """
    Создание нового ресторана.
    """

    model = Restaurant
    form_class = RestaurantForm
    success_url = reverse_lazy("restaurant_list")


class RestaurantDetailView(DetailView):
    """
    Подробная информация о ресторане.
    """

    model = Restaurant
    template_name = "restaurants/restaurant_detail.html"


class RestaurantUpdateView(SuperUserRequiredMixin, UpdateView):
    """
    Редактирование ресторана.
    """

    model = Restaurant
    form_class = RestaurantForm
    success_url = reverse_lazy("restaurants:restaurant_list")


class RestaurantDeleteView(SuperUserRequiredMixin, DeleteView):
    """
    Удаление ресторана.
    """

    model = Restaurant
    template_name = "restaurants/restaurant_confirm_delete.html"
    success_url = reverse_lazy("restaurants:restaurant_list")


class ReserveCreateView(LoginRequiredMixin, CreateView):
    """
    Создание бронирования.
    """

    model = Reserve
    form_class = ReserveForm
    success_url = reverse_lazy("restaurants:reserve_list")

    def get_initial(self):
        initial = super().get_initial()
        table_id = self.kwargs.get("table_id")
        if table_id:
            initial["table"] = Table.objects.get(id=table_id)
        return initial

    def form_valid(self, form):
        reserve = form.save(commit=False)
        reserve.client = self.request.user

        """
        Проверка доступности стола
        """

        if reserve.date_reserved < timezone.now().date():
            messages.error(self.request, "Нельзя бронировать на прошедшую дату.")
            return self.form_invalid(form)

        reserve_datetime = datetime.combine(
            reserve.date_reserved, reserve.time_reserved
        )
        start_time = reserve_datetime - timedelta(hours=2)
        end_time = reserve_datetime + timedelta(hours=2)

        conflicting_reservations = Reserve.objects.filter(
            table=reserve.table,
            date_reserved=reserve.date_reserved,
            time_reserved__range=(start_time.time(), end_time.time()),
            is_active=True,
        )
        if conflicting_reservations.exists():
            messages.error(
                self.request, "Этот стол уже забронирован на выбранное время."
            )
            return self.form_invalid(form)

        reserve.save()
        messages.success(self.request, "Бронирование успешно создано.")
        return super().form_valid(form)


class ReserveUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирование бронирования
    """

    model = Reserve
    form_class = ReserveUpdateForm
    success_url = reverse_lazy("restaurants:reserve_list")

    def form_valid(self, form):
        """
        Переопределение формы валидации.
        Присваивание текущего пользователя к бронированию.
        Логирование данные перед сохранением.
        """
        reserve = form.save(commit=False)
        reserve.client = self.request.user

        reserve.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Вывод ошибки формы.
        """
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Дополнительная информация
        """
        context = super().get_context_data(**kwargs)
        table = Table.objects.get(pk=self.object.table.pk)

        context["table"] = table
        context["date"] = self.object.date_reserved
        context["is_edit"] = True

        return context


class ReserveListView(LoginRequiredMixin, ListView):
    """
    Просмотр списка бронирований.
    """

    model = Reserve
    template_name = "restaurants/reserve_list.html"
    context_object_name = "reserved"

    def get_queryset(self):
        """
        Возвращает только бронирования текущего пользователя.
        """
        return Reserve.objects.filter(client=self.request.user)


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    form_class = FeedbackForm
    template_name = "restaurants/feedback_form.html"
    success_url = reverse_lazy("restaurants:feedback_success")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        restaurant_id = self.kwargs.get("restaurant_id")
        if restaurant_id:
            kwargs["restaurant"] = get_object_or_404(Restaurant, id=restaurant_id)
        return kwargs

    def form_valid(self, form):
        feedback = form.save(commit=False)
        feedback.user = self.request.user
        if hasattr(form, "restaurant") and form.restaurant:
            feedback.restaurant = form.restaurant
        feedback.save()
        messages.success(
            self.request, "Спасибо за ваш отзыв! Мы свяжемся с вами в ближайшее время."
        )
        return super().form_valid(form)

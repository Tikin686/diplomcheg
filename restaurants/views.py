from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from config import settings
from restaurants.forms import RestaurantForm, TableForm, ReserveForm, ReserveUpdateForm
from restaurants.models import Restaurant, Table, Reserve, ReserveHistory
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils import timezone
from datetime import datetime, timedelta
from restaurants.templatetags.my_tags import formatting_date, formatting_time
from django.contrib import messages
from django.apps import apps


class ReserveCancelView(LoginRequiredMixin, View):
    def get(self, request, pk):
        reserve = get_object_or_404(Reserve, pk=pk, client=request.user)
        if reserve.is_active:
            reserve.is_active = False
            reserve.save()
            messages.success(request, "Бронирование успешно отменено.")
        else:
            messages.warning(request, "Это бронирование уже отменено.")
        return redirect('restaurants:reserve_list')


class RestaurantListView(ListView):
    model = Restaurant
    template_name = "restaurant_list.html"


class RestaurantCreateView(CreateView):
    model = Restaurant
    form_class = RestaurantForm
    success_url = reverse_lazy("restaurant_list")


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "restaurants/restaurant_detail.html"


class RestaurantUpdateView(UpdateView):
    model = Restaurant
    form_class = RestaurantForm
    success_url = reverse_lazy("restaurants:restaurant_list")


class RestaurantDeleteView(DeleteView):
    model = Restaurant
    template_name = "restaurants/restaurant_confirm_delete.html"
    success_url = reverse_lazy("restaurants:restaurant_list")


class ReserveCreateView(LoginRequiredMixin, CreateView):
    """
    Создание бронирования.
    """
    model = Reserve
    form_class = ReserveForm
    success_url = reverse_lazy('restaurants:reserve_list')

    def get_initial(self):
        initial = super().get_initial()
        table_id = self.kwargs.get('table_id')
        if table_id:
            initial['table'] = Table.objects.get(id=table_id)
        return initial

    def form_valid(self, form):
        reserve = form.save(commit=False)
        reserve.client = self.request.user

        """
        Проверка доступности стола
        """

        # Проверка, не прошла ли дата бронирования
        if reserve.date_reserved < timezone.now().date():
            messages.error(self.request, "Нельзя бронировать на прошедшую дату.")
            return self.form_invalid(form)

            # Проверка доступности стола
        reserve_datetime = datetime.combine(reserve.date_reserved, reserve.time_reserved)
        start_time = reserve_datetime - timedelta(hours=2)
        end_time = reserve_datetime + timedelta(hours=2)

        conflicting_reservations = Reserve.objects.filter(
            table=reserve.table,
            date_reserved=reserve.date_reserved,
            time_reserved__range=(start_time.time(), end_time.time()),
            is_active=True
        )
        if conflicting_reservations.exists():
            messages.error(self.request, "Этот стол уже забронирован на выбранное время.")
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
    success_url = reverse_lazy('restaurants:reserve_list')

    def form_valid(self, form):
        """
        Переопределение формы валидации.
        Присваивание текущего пользователя к бронированию.
        Логирование данные перед сохранением.
        """
        reserve = form.save(commit=False)
        reserve.client = self.request.user

        print(f"Дата бронирования: {reserve.date_reserved}")
        print(f"Время бронирования: {reserve.time_reserved}")
        print(f"Стол: {reserve.table}")
        print(f"Клиент: {reserve.client}")

        reserve.save()

        return super().form_valid(form)


    def form_invalid(self, form):
        """
        Вывод ошибки формы.
        """
        print('Форма не прошла валидацию. Ошибки:', form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Дополнительная информация
        """
        context = super().get_context_data(**kwargs)
        table = Table.objects.get(pk=self.object.table.pk)

        context['table'] = table
        context['date'] = self.object.date_reserve
        context['is_edit'] = True

        return context


class ReserveListView(LoginRequiredMixin, ListView):
    """
    Просмотр списка бронирований.
    """
    model = Reserve
    template_name = 'restaurants/reserve_list.html'
    context_object_name = 'reserved'

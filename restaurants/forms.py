from django import forms
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from restaurants.models import Restaurant, Reserve
from django.utils import timezone
from datetime import timedelta


class RestaurantForm(forms.ModelForm):
    """
    Форма ресторана.
    """
    class Meta:
        model = Restaurant
        exclude = ("free_seats", )


class StyleFormMixin:
    """
    Стилизация формы
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class TableForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для выбора стола с временными интервалами бронирования
    """
    open_time = 10
    close_reserve_time = 20
    time_step = 30

    next_day = timezone.localdate() + timedelta(days=1)

    date_reserve = forms.DateField(label='Дата бронирования', widget=forms.DateInput(
        attrs={'type': 'date',
               'min': next_day.strftime('%Y-%m-%d'),
               'max': (next_day + timedelta(days=6)).strftime('%Y-%m-%d'),
               }),
    )

    class Meta:
        model = Reserve
        fields = ['date_reserved']


class ReserveForm(StyleFormMixin, forms.ModelForm):
    """
    Форма бронирования
    """
    time_reserved = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Reserve
        fields = ['date_reserved', 'time_reserved', 'table']


class ReserveUpdateForm(StyleFormMixin, forms.ModelForm):
    """
    Форма редактирования бронирования
    """
    open_time = 10
    close_reserve_time = 20
    time_step = 30

    next_day = timezone.localdate() + timedelta(days=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')

        if instance:
            self.initial['date_reserved'] = instance.date_reserved

    class Meta:
        model = Reserve
        exclude = ('is_active', 'client')


class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        raise PermissionDenied("У вас нет разрешения на выполнение этого действия.")
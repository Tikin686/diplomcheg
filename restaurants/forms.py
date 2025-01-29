from django import forms
from restaurants.models import Restaurant, Reserve
from django.utils import timezone
from datetime import datetime, timedelta


class RestaurantForm(forms.ModelForm):
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

    #def __init__(self, *args, **kwargs):
        #super(TableForm, self).__init__(*args, **kwargs)

        #times = [
            #(datetime.strptime(f'{hour:02d}:{minute:02d}', '%H:%M').time(), f'{hour:02d}:{minute:02d}')
            #for hour in range(self.open_time, self.close_reserve_time + 1) for minute in [0, self.time_step]
            #if hour < self.close_reserve_time or (hour == self.close_reserve_time and minute == 0)
        #]

        #self.fields['time_reserved'].choices = times

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
            self.initial['date_reserve'] = instance.date_reserve


        all_times = [
            (datetime.strptime(f'{hour:02d}:{minute:02d}', '%H:%M').time(), f'{hour:02d}:{minute:02d}')
            for hour in range(self.open_time, self.close_reserve_time + 1) for minute in [0, self.time_step]
            if hour < self.close_reserve_time or (hour == self.close_reserve_time and minute == 0)
        ]

        """
        Получаем занятые времена и даты на стол
        """
        reserve_times = self.get_reserve_times(instance.table, self.initial.get('date_reserve', self.next_day))

        """
        Фильтр временного списка(Оставляем свободное)
        """
        available_times = [(t, s) for t, s in all_times if (t, s) not in reserve_times]


    #@staticmethod
    #def get_reserve_times(table, date):
        #"""
        #Возвращает список занятого времени и даты для определенного стола.
        #Реализовываем запрос к БД.
        #"""
        #reserve_slots = Reserve.objects.filter(table=table, date_reserved=date).values_list('time_reserved', flat=True)
        #return [(datetime.strptime(str(slot), '%H:%M:%S').time(), str(slot)[:5]) for slot in reserve_slots]

    class Meta:
        model = Reserve
        fields = '__all__'

from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Restaurant(models.Model):
    """
    Ресторан.
    """
    name = models.CharField(max_length=50, verbose_name='Название ресторана')
    phone_number = PhoneNumberField(default='+7', unique=True, verbose_name='Номер телефона')
    address = models.CharField(max_length=250, unique=True, verbose_name='Адрес')
    description = models.TextField(verbose_name='Описание ресторана')
    history = models.TextField(verbose_name='История ресторана', **NULLABLE)
    mission = models.TextField(verbose_name='Миссия ресторана', **NULLABLE)
    command = models.TextField(verbose_name='Команда', **NULLABLE)
    services = models.TextField(verbose_name='Предоставляемые услуги')
    total_seats = models.PositiveIntegerField(verbose_name='Общее количество мест')
    free_seats = models.PositiveIntegerField(verbose_name='Количество свободных мест')
    reserved_seats = models.PositiveIntegerField(verbose_name='Количество занятых мест', **NULLABLE)
    photo = models.ImageField(upload_to='restaurant/photo', **NULLABLE, verbose_name='Фото', help_text='Загрузите фото ресторана')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'


class Table(models.Model):
    """
    Стол.
    """
    number = models.PositiveIntegerField(verbose_name='Номер стола')
    total_seats = models.PositiveIntegerField(verbose_name='Общее количество мест')
    reserved_seats = models.BooleanField(verbose_name='Забронированные места', default=False)
    table_size = models.PositiveIntegerField(verbose_name='Размер стола', **NULLABLE, help_text='Количество мест за столом')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='tables', verbose_name='Ресторан', default=1)

    def __str__(self):
        return f'{self.number} в ресторане {self.table_size}'

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'


class AbstractReserve(models.Model):
    """
    Абстрактная модель для бронирования столов в ресторане.
    """
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, verbose_name='Стол', **NULLABLE)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Клиент', **NULLABLE)
    date_reserved = models.DateField(verbose_name='Дата бронирования')
    time_reserved = models.TimeField(verbose_name='Время бронирования')
    duration_reserved = models.PositiveIntegerField(verbose_name='Продолжительность бронирования', default=3)
    created_reserve = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания брони')
    message = models.TextField(verbose_name='Сообщение', **NULLABLE)

    def __str__(self):
        table_number = self.table.number if self.table else 'Неизвестный стол'
        return f'Бронирование стола {table_number} на {self.date_reserved} и {self.time_reserved}'

    class Meta:
        abstract = True


class Reserve(AbstractReserve):
    """
    Модель бронирования стола.
    """
    is_active = models.BooleanField(verbose_name='Активная бронь', default=True)
    objects = models.Manager()
    #name = models.CharField(max_length=50, verbose_name='Название', help_text='Напишите название ресторана')
    #number = models.IntegerField(verbose_name='Номер стола')
    #table_size = models.PositiveIntegerField(verbose_name='Размер стола', **NULLABLE)
    #start_reserve = models.PositiveIntegerField(verbose_name='Начало бронирования', **NULLABLE)
    #end_reserve = models.PositiveIntegerField(verbose_name='Окончание бронирования', **NULLABLE)

    #def __str__(self):
    #    return f'{self.name} {self.start_reserve}-{self.end_reserve}'

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def cancel_reserve(self):
        """
        Отмена бронирования.
        """
        ReserveHistory.objects.create(
            table=self.table,
            client=self.client,
            date_reserved=self.date_reserved,
            time_reserved=self.time_reserved,
            duration_reserved=self.duration_reserved,
            message=self.message,
            cancel_reserve=timezone.now()
        )

        if self.table:
            self.table.is_reserved_seats = False
            self.table.save()

        self.delete()


class ReserveHistory(AbstractReserve):
    """
    История бронирования.
    """
    cancel_reserve = models.DateTimeField(verbose_name="Время отмены бронирования")
    objects = models.Manager()

    class Meta:
        verbose_name = 'История бронирования'
        verbose_name_plural = 'История бронирований'
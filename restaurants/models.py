from django.db import models

NULLABLE = {"null": True, "blank": True}


class Restaurant(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название', help_text='Напишите название ресторана')
    phone = models.CharField(max_length=15, verbose_name='Номер телефона', help_text='Введите номер ресторана')
    address = models.CharField(max_length=250, verbose_name='Адрес', help_text='Введите адрес ресторана')
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
    name = models.CharField(max_length=50, verbose_name='Название', help_text='Напишите название ресторана')
    total_seats = models.PositiveIntegerField(verbose_name='Общее количество мест')
    free_seats = models.PositiveIntegerField(verbose_name='Количество свободных мест')
    reserved_seats = models.PositiveIntegerField(verbose_name='Количество занятых мест', **NULLABLE)
    table_number = models.PositiveIntegerField(verbose_name='Номер стола')
    table_size = models.PositiveIntegerField(verbose_name='Размер стола', **NULLABLE, help_text='Количество мест за столом')

    def __str__(self):
        return f'{self.table_number} {self.table_size}'

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'


class Reserve(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название', help_text='Напишите название ресторана')
    table_number = models.PositiveIntegerField(verbose_name='Номер стола')
    table_size = models.PositiveIntegerField(verbose_name='Размер стола', **NULLABLE)
    start_reserve = models.PositiveIntegerField(verbose_name='Начало бронирования', **NULLABLE)
    end_reserve = models.PositiveIntegerField(verbose_name='Окончание бронирования', **NULLABLE)

    def __str__(self):
        return f'{self.name} {self.start_reserve}-{self.end_reserve}'

    class Meta:
        verbose_name = 'Резерв'
        verbose_name_plural = 'Резервы'
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
    reserved_seats = models.PositiveIntegerField(verbose_name='Количество занятых мест', null=True, blank=True)
    photo = models.ImageField(upload_to='restaurant/photo', blank=True, null=True, verbose_name='Фото', help_text='Загрузите фото ресторана')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'
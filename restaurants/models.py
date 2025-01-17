from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    phone = models.CharField(max_length=15, verbose_name="Номер телефона")
    address = models.CharField(max_length=250, verbose_name="Адрес")
    description = models.TextField(verbose_name="Описание ресторана")
    history = models.TextField(verbose_name="История ресторана")
    mission = models.TextField(verbose_name="Миссия ресторана")
    command = models.TextField(verbose_name="Команда")
    services = models.TextField(verbose_name="Предоставляемые услуги")
    total_seats = models.PositiveIntegerField(verbose_name="Общее количество мест")
    free_seats = models.PositiveIntegerField(verbose_name="Количество свободных мест")

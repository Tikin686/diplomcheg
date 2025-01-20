# Generated by Django 4.2.2 on 2025-01-20 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Напишите название ресторана",
                        max_length=50,
                        verbose_name="Название",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        help_text="Введите номер ресторана",
                        max_length=15,
                        verbose_name="Номер телефона",
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        help_text="Введите адрес ресторана",
                        max_length=250,
                        verbose_name="Адрес",
                    ),
                ),
                ("description", models.TextField(verbose_name="Описание ресторана")),
                (
                    "history",
                    models.TextField(
                        blank=True, null=True, verbose_name="История ресторана"
                    ),
                ),
                (
                    "mission",
                    models.TextField(
                        blank=True, null=True, verbose_name="Миссия ресторана"
                    ),
                ),
                (
                    "command",
                    models.TextField(blank=True, null=True, verbose_name="Команда"),
                ),
                ("services", models.TextField(verbose_name="Предоставляемые услуги")),
                (
                    "total_seats",
                    models.PositiveIntegerField(verbose_name="Общее количество мест"),
                ),
                (
                    "free_seats",
                    models.PositiveIntegerField(
                        verbose_name="Количество свободных мест"
                    ),
                ),
                (
                    "reserved_seats",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Количество занятых мест"
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите фото ресторана",
                        null=True,
                        upload_to="restaurant/photo",
                        verbose_name="Фото",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ресторан",
                "verbose_name_plural": "Рестораны",
            },
        ),
    ]

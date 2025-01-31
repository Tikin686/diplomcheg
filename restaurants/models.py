from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from users.models import User

NULLABLE = {"null": True, "blank": True}


class Restaurant(models.Model):
    """
    Ресторан.
    """

    name = models.CharField(
        max_length=50, unique=True, verbose_name="Название ресторана"
    )
    phone_number = PhoneNumberField(
        default="+7", unique=True, verbose_name="Номер телефона"
    )
    address = models.CharField(max_length=250, unique=True, verbose_name="Адрес")
    description = models.TextField(verbose_name="Описание ресторана")
    history = models.TextField(verbose_name="История ресторана", **NULLABLE)
    mission = models.TextField(verbose_name="Миссия ресторана", **NULLABLE)
    command = models.TextField(verbose_name="Команда", **NULLABLE)
    services = models.TextField(verbose_name="Предоставляемые услуги")
    photo = models.ImageField(
        upload_to="restaurant/photo",
        **NULLABLE,
        verbose_name="Фото",
        help_text="Загрузите фото ресторана",
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Ресторан"
        verbose_name_plural = "Рестораны"


class Table(models.Model):
    """
    Модель стола.
    """

    number = models.PositiveIntegerField(verbose_name="Номер стола")
    seats = models.PositiveIntegerField(verbose_name="Общее количество мест")
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="tables",
        verbose_name="Ресторан",
    )

    def __str__(self):
        return f"Стол {self.number} в {self.restaurant.name}"

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"
        unique_together = ["number", "restaurant"]


class Reserve(models.Model):
    """
    Модель бронирования стола.
    """

    is_active = models.BooleanField(verbose_name="Активная бронь", default=True)
    date_reserved = models.DateField(verbose_name="Дата бронирования")
    time_reserved = models.TimeField(verbose_name="Время бронирования")
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="clients",
        verbose_name="Клиент",
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        null=True,
        related_name="tables",
        verbose_name="Стол",
    )
    duration = models.DurationField(
        default=timezone.timedelta(hours=2), verbose_name="Продолжительность"
    )

    def __str__(self):
        return (
            f"Бронирование {self.client} на {self.date_reserved} {self.time_reserved}"
        )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def cancel(self):
        """
        Отмена бронирования.
        """
        self.is_active = False
        self.save()
        ReserveHistory.objects.create(reservation=self, cancelled_at=timezone.now())


class ReserveHistory(models.Model):
    """
    История бронирования.
    """

    reservation = models.ForeignKey(
        Reserve,
        on_delete=models.CASCADE,
        related_name="history",
        verbose_name="Бронирование",
    )
    cancelled_at = models.DateTimeField(verbose_name="Время отмены бронирования")

    class Meta:
        verbose_name = "История бронирования"
        verbose_name_plural = "История бронирований"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client")
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="restaurant",
    )
    subject = models.CharField(max_length=200, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"

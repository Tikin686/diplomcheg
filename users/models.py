from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    """
    Пользователь
    """
    username = None
    email = models.EmailField(verbose_name='Ваша почта', unique=True)
    first_name = models.TextField(verbose_name='Введите имя', max_length=50)
    last_name = models.TextField(verbose_name='Введите фамилию', max_length=50)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    token = models.CharField(max_length=100, verbose_name='Токен', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f'{self.first_name}{self.last_name}'

    def __repr__(self):
        return f'{self.email}'
from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.TextField(verbose_name='Введите имя', max_length=50)
    last_name = models.TextField(verbose_name='Введите фамилию', max_length=50)
    phone = models.CharField(max_length=20)
    token = models.CharField(max_length=100, verbose_name='Токен', **NULLABLE)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
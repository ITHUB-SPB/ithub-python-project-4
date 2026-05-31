from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Teacher(models.Model):
    last_name = models.CharField(max_length=40, verbose_name='фамилия')
    first_name = models.CharField(max_length=20, verbose_name='имя')
    patronymic = models.CharField(max_length=40, blank=True, null=True, verbose_name='отчество')
    account = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='аккаунт')

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        ordering = ['last_name', 'first_name', 'patronymic']

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Manager(models.Model):
    last_name = models.CharField(max_length=40, verbose_name='фамилия')
    first_name = models.CharField(max_length=20, verbose_name='имя')
    patronymic = models.CharField(max_length=40, blank=True, null=True, verbose_name='отчество')
    account = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='аккаунт')

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'
        ordering = ['last_name', 'first_name', 'patronymic']

    def __str__(self):
        return f'{self.last_name} {self.first_name}'
from django.contrib.auth import get_user_model
from django.db import models


class Teacher(models.Model):
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=40, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=40, null=True, blank=True, verbose_name='Отчество')

    account = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,verbose_name='Аккаунт')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        ordering = ['-last_name', '-first_name', '-middle_name']


class Manager(models.Model):
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=40, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=40, null=True, blank=True, verbose_name='Отчество')

    account = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name='Аккаунт')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'
        ordering = ['-last_name', '-first_name', '-middle_name']
from django.db import models
from django.conf import settings

class Teacher(models.Model):
    first_name = models.CharField(
        max_length=20,
        verbose_name='имя'
    )

    last_name = models.CharField(
        max_length=40,
        verbose_name='фамилия'
    )

    middle_name = models.CharField(
        max_length=40,
        blank=True,
        verbose_name='отчество'
    )

    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='аккаунт'
    )

    class Meta:
        verbose_name = 'преподаватель'
        verbose_name_plural = 'преподаватели'
        ordering = ['last_name', 'first_name', 'middle_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Manager(models.Model):
    first_name = models.CharField(
        max_length=20,
        verbose_name='имя'
    )

    last_name = models.CharField(
        max_length=40,
        verbose_name='фамилия'
    )
    
    middle_name = models.CharField(
        max_length=40,
        blank=True,
        verbose_name='отчество'
    )
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='аккаунт'
    )

    class Meta:
        verbose_name = 'менеджер'
        verbose_name_plural = 'менеджеры'
        ordering = ['last_name', 'first_name', 'middle_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name}'
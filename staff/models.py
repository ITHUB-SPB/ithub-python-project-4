from django.db import models
from django.conf import settings

class Teacher(models.Model):
    last_name = models.CharField(
        max_length=40,
        verbose_name='фамилия'
    )
    first_name = models.CharField(
        max_length=20,
        verbose_name='имя'
    )
    patronymic = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name='отчество'
    )
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        verbose_name='аккаунт'
    )
    
    class Meta:
        verbose_name = 'преподаватель'
        verbose_name_plural = 'преподаватели'
        ordering = ['last_name', 'first_name', 'patronymic']
    
    def __str__(self):
        if self.patronymic:
            return f"{self.last_name} {self.first_name} {self.patronymic}"
        return f"{self.last_name} {self.first_name}"
    
    @property
    def full_name(self):
        return str(self)


class Manager(models.Model):
    last_name = models.CharField(
        max_length=40,
        verbose_name='фамилия'
    )
    first_name = models.CharField(
        max_length=20,
        verbose_name='имя'
    )
    patronymic = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name='отчество'
    )
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='manager_profile',
        verbose_name='аккаунт'
    )
    
    class Meta:
        verbose_name = 'менеджер'
        verbose_name_plural = 'менеджеры'
        ordering = ['last_name', 'first_name', 'patronymic']
    
    def __str__(self):
        if self.patronymic:
            return f"{self.last_name} {self.first_name} {self.patronymic}"
        return f"{self.last_name} {self.first_name}"
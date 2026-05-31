from django.db import models
from django.conf import settings


class Teacher(models.Model):
    first_name = models.CharField(max_length=20, verbose_name="Имя")
    last_name = models.CharField(max_length=40, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=40, null=True, blank=True, verbose_name="Отчество")
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Аккаунт")

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ["-last_name", "-first_name", "-middle_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Manager(models.Model):
    first_name = models.CharField(max_length=20, verbose_name="Имя")
    last_name = models.CharField(max_length=40, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=40, null=True, blank=True, verbose_name="Отчество")
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Аккаунт")

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"
        ordering = ["-last_name", "-first_name", "-middle_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

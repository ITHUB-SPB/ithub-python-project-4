from django.conf import settings
from django.db import models


class Teacher(models.Model):
    first_name = models.CharField(max_length=20, verbose_name="имя")
    last_name = models.CharField(max_length=40, verbose_name="фамилия")
    patronymic = models.CharField(max_length=40, blank=True, verbose_name="отчество")
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher",
        verbose_name="аккаунт",
    )

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ["last_name", "first_name", "patronymic"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Manager(models.Model):
    first_name = models.CharField(max_length=20, verbose_name="имя")
    last_name = models.CharField(max_length=40, verbose_name="фамилия")
    patronymic = models.CharField(max_length=40, blank=True, verbose_name="отчество")
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="manager",
        verbose_name="аккаунт",
    )

    class Meta:
        verbose_name = "Менеджер учебной части"
        verbose_name_plural = "Менеджеры учебной части"
        ordering = ["last_name", "first_name", "patronymic"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

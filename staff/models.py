from django.db import models
from django.conf import settings


class Teacher(models.Model):
    first_name = models.CharField("Имя", max_length=20, null=False)
    last_name = models.CharField("Фамилия", max_length=40, null=False)
    middle_name = models.CharField("Отчество", max_length=40, null=True, blank=True)

    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher",
        verbose_name="Аккаунт",
    )

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ["last_name", "first_name", "middle_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Manager(models.Model):
    first_name = models.CharField("Имя", max_length=20, null=False)
    last_name = models.CharField("Фамилия", max_length=40, null=False)
    middle_name = models.CharField("Отчество", max_length=40, null=True, blank=True)

    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="manager",
        verbose_name="Аккаунт",
    )

    class Meta:
        verbose_name = "Менеджер учебной части"
        verbose_name_plural = "Менеджеры учебной части"
        ordering = ["last_name", "first_name", "middle_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

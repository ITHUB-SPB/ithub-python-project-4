from django.db import models
from django.conf import settings


class Group(models.Model):
    COURSES = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
    ]

    title = models.CharField(max_length=15, verbose_name="название")
    course = models.CharField(max_length=1, choices=COURSES, verbose_name="курс")

    class Meta:
        verbose_name = "Учебная группа"
        verbose_name_plural = "Учебные группы"
        ordering = ["course"]
        indexes = [
            models.Index(fields=["course"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.course})"


class Student(models.Model):
    first_name = models.CharField(max_length=20, verbose_name="имя")
    last_name = models.CharField(max_length=40, verbose_name="фамилия")
    patronymic = models.CharField(max_length=40, blank=True, verbose_name="отчество")
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student",
        verbose_name="аккаунт",
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
        verbose_name="группа",
    )

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

from django.db import models
from django.conf import settings


COURSE_CHOICES = [
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
]


class Group(models.Model):
    title = models.CharField(max_length=15, verbose_name="Название")
    course = models.CharField(max_length=1, choices=COURSE_CHOICES, verbose_name="Курс")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        ordering = ["course"]
        indexes = [models.Index(fields=["course"])]

    def __str__(self):
        return self.title


class Student(models.Model):
    first_name = models.CharField(max_length=20, verbose_name="Имя")
    last_name = models.CharField(max_length=40, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=40, null=True, blank=True, verbose_name="Отчество")
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Аккаунт")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Группа")

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ["last_name", "first_name"]
        indexes = [models.Index(fields=["last_name", "first_name"])]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

from django.db import models
from django.conf import settings

class Group(models.Model):
    class Course(models.TextChoices):
        first = '1'
        second = '2'
        third = '3'
        fourth = '4'

    title = models.CharField(max_length=15, unique=True, null=False)
    course = models.CharField(choices=Course, null=False)

    class Meta:
        verbose_name = "Учебная группа"
        verbose_name_plural = "Учебные группы"
        ordering = ['course']
        indexes = [
            models.Index(fields=['course']),
        ]

    def __str__(self):
        return self.title

class Student(models.Model):
    first_name = models.CharField("Имя",max_length=20, null=False)
    last_name = models.CharField("Фамилия",max_length=40, null=False)
    middle_name = models.CharField("Отчество",max_length=40, null=True, blank=True)

    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student",
        verbose_name="Аккаунт"
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
        verbose_name="Учебная группа"
    )

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=["group"])
        ]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

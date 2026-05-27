from django.db import models
from django.contrib.auth import get_user_model

class Group(models.Model):
    class Year(models.TextChoices):
        first = '1', '1 курс'
        second = '2', '2 курс'
        third = '3', '3 курс'
        four = '4', '4 курс'
    title = models.CharField(max_length=15, null=False, unique=True, verbose_name="Группа")
    year = models.CharField(choices=Year, null=False, verbose_name="Курс")

    class Meta:
        ordering = ['year', '-title']
        indexes = [
            models.Index(fields=['year'])
        ]
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

class Student(models.Model):
    first_name = models.CharField(max_length=20, null=False, verbose_name="Имя")
    last_name = models.CharField(max_length=40, null=False, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=40, null=True, blank=True, verbose_name="Отчество")
    account = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=False, verbose_name="Аккаунт")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, verbose_name="Группа")

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        indexes = [
            models.Index(fields=['group'])
        ]
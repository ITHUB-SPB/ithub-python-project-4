from django.contrib.auth import get_user_model
from django.db import models


class Course(models.TextChoices):
    FIRST = '1', 'I'
    SECOND = '2', 'II'
    THIRD = '3', 'III'
    FOURTH = '4', 'IV'


class Group(models.Model):
    title = models.CharField(max_length=15, unique=True, verbose_name='Название')

    course = models.CharField(max_length=1, choices=Course.choices, verbose_name='Курс')

    def __str__(self):
        return f'{self.title} ({self.course})'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['course']
        indexes = [
            models.Index(fields=['course']),
        ]


class Student(models.Model):
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=40, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=40, null=True, blank=True, verbose_name='Отчество')
    
    account = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name='Аккаунт')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Группа')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['last_name', 'first_name']
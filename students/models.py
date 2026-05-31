from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    COURSE_CHOICES = [
        (1, '1 курс'),
        (2, '2 курс'),
        (3, '3 курс'),
        (4, '4 курс'),
    ]

    name = models.CharField(max_length=15, verbose_name='название')
    course = models.IntegerField(choices=COURSE_CHOICES, verbose_name='курс')

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'
        ordering = ['course']
        indexes = [
            models.Index(fields=['course']),
        ]

    def __str__(self):
        return self.name


class Student(models.Model):
    last_name = models.CharField(max_length=40, verbose_name='фамилия')
    first_name = models.CharField(max_length=20, verbose_name='имя')
    patronymic = models.CharField(max_length=40, blank=True, null=True, verbose_name='отчество')
    account = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='аккаунт')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, verbose_name='группа')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
        ]

    def __str__(self):
        return f'{self.last_name} {self.first_name}'
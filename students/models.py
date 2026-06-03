from django.db import models
from django.conf import settings

class Group(models.Model):
    COURSE_CHOICES = [
        ('1', '1 курс'),
        ('2', '2 курс'),
        ('3', '3 курс'),
        ('4', '4 курс'),
    ]

    title = models.CharField(
        max_length=15,
        verbose_name='название'
    )

    course = models.CharField(
        max_length=1,
        choices=COURSE_CHOICES,
        verbose_name='курс'
    )

    class Meta:
        verbose_name = 'учебная группа'
        verbose_name_plural = 'учебные группы'
        ordering = ['course']
        indexes = [
            models.Index(fields=['course']),
        ]

    def __str__(self):
        return self.title


class Student(models.Model):
    first_name = models.CharField(
        max_length=20,
        verbose_name='имя'
    )

    last_name = models.CharField(
        max_length=40,
        verbose_name='фамилия'
    )

    middle_name = models.CharField(
        max_length=40,
        blank=True,
        verbose_name='отчество'
    )

    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='аккаунт'
    )
    
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='учебная группа'
    )

    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'студенты'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name}'
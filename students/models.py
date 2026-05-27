from django.conf import settings
from django.db import models


class Group(models.Model):
    class CourseChoices(models.TextChoices):
        FIRST = '1', '1 курс'
        SECOND = '2', '2 курс'
        THIRD = '3', '3 курс'
        FOURTH = '4', '4 курс'

    title = models.CharField(
        max_length=15,
        verbose_name='Название группы'
    )

    course = models.CharField(
        max_length=1,
        choices=CourseChoices.choices,
        verbose_name='Курс',
        db_index=True
    )

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'
        ordering = ['course']
        indexes = [
            models.Index(fields=['course'], name='group_course_idx'),
        ]

    def __str__(self):
        return f'{self.title} ({self.get_course_display()})'


class Student(models.Model):
    first_name = models.CharField(
        max_length=20,
        verbose_name='Имя'
    )

    last_name = models.CharField(
        max_length=40,
        verbose_name='Фамилия'
    )

    middle_name = models.CharField(
        max_length=40,
        blank=True,
        verbose_name='Отчество'
    )

    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student',
        verbose_name='Аккаунт'
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name='Группа'
    )

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        if self.middle_name:
            return f'{self.last_name} {self.first_name} {self.middle_name}'
        return f'{self.last_name} {self.first_name}'
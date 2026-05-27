from django.core.validators import MinValueValidator
from django.db import models

from students.models import Group
from staff.models import Teacher


class Discipline(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Название дисциплины'
    )

    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Длительность'
    )

    curriculum = models.FileField(
        upload_to='curriculums/',
        null=True,
        blank=True,
        verbose_name='Учебный план'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
        ordering = ['updated_at', 'created_at']
        indexes = [
            models.Index(fields=['title'], name='discipline_title_idx'),
        ]

    def __str__(self):
        return f'{self.title} ({self.duration} ч.)'


class Course(models.Model):
    code = models.CharField(
        max_length=15,
        verbose_name='Код курса',
        db_index=True
    )

    about = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Описание курса'
    )

    course_start = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата начала'
    )

    course_end = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата окончания'
    )

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name='Дисциплина'
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name='Группа'
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name='Преподаватель'
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['discipline__title', 'code']
        indexes = [
            models.Index(fields=['code'], name='course_code_idx'),
            models.Index(fields=['course_start'], name='course_start_idx'),
            models.Index(fields=['course_end'], name='course_end_idx'),
        ]

    def __str__(self):
        if self.discipline:
            return f'{self.code} — {self.discipline.title}'
        return self.code
from django.db import models
from django.conf import settings
from students.models import Group

class Discipline(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='название дисциплины'
    )
    duration = models.PositiveIntegerField(
        verbose_name='длительность (часы)'
    )
    curriculum = models.FileField(
        upload_to='curricula/',
        blank=True,
        null=True,
        verbose_name='учебный план'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='дата обновления'
    )
    
    class Meta:
        verbose_name = 'дисциплина'
        verbose_name_plural = 'дисциплины'
        ordering = ['-updated_at', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.duration}ч)"


class Course(models.Model):
    code = models.CharField(
        max_length=15,
        unique=True,
        verbose_name='код курса'
    )
    about = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='описание курса'
    )
    course_start = models.DateField(
        blank=True,
        null=True,
        verbose_name='дата начала'
    )
    course_end = models.DateField(
        blank=True,
        null=True,
        verbose_name='дата завершения'
    )
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses',
        verbose_name='дисциплина'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name='учебная группа'
    )
    teacher = models.ForeignKey(
        'staff.Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name='преподаватель'
    )
    
    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ['discipline__code']
        indexes = [
            models.Index(fields=['discipline']),
            models.Index(fields=['group']),
            models.Index(fields=['teacher']),
            models.Index(fields=['course_start', 'course_end']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.discipline.title if self.discipline else 'Без дисциплины'}"
    
class Topic(models.Model):
    ordering_number = models.PositiveIntegerField(
        verbose_name='порядковый номер'
    )
    title = models.CharField(
        max_length=50,
        verbose_name='название темы'
    )
    content = models.TextField(
        verbose_name='содержание'
    )
    duration = models.PositiveIntegerField(
        verbose_name='часы на изучение'
    )
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.SET_NULL,
        null=True,
        related_name='topics',
        verbose_name='дисциплина'
    )
    
    class Meta:
        verbose_name = 'учебная тема'
        verbose_name_plural = 'учебные темы'
        ordering = ['discipline__code', 'ordering_number']
        unique_together = [['ordering_number', 'discipline']]
        indexes = [
            models.Index(fields=['discipline', 'ordering_number']),
        ]
    
    def __str__(self):
        return f"{self.ordering_number}. {self.title}"
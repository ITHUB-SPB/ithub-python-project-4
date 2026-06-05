from django.db import models
from students.models import Group
from staff.models import Teacher


class Discipline(models.Model):
    title = models.CharField(max_length=50, verbose_name='название дисциплины')
    duration = models.PositiveIntegerField(verbose_name='длительность (часов)')
    curriculum = models.FileField(upload_to='curricula/', blank=True, null=True, verbose_name='учебный план')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата обновления')

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.title


class Course(models.Model):
    code = models.CharField(max_length=15, verbose_name='код курса')
    about = models.CharField(max_length=200, blank=True, null=True, verbose_name='описание')
    course_start = models.DateField(blank=True, null=True, verbose_name='дата начала')
    course_end = models.DateField(blank=True, null=True, verbose_name='дата завершения')
    discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True, verbose_name='дисциплина')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='группа', related_name='courses')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, verbose_name='преподаватель')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['discipline__title']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['discipline']),
            models.Index(fields=['group']),
        ]

    def __str__(self):
        return self.code


class Topic(models.Model):
    """Учебная тема"""
    course = models.ForeignKey(
        'Course', 
        on_delete=models.CASCADE, 
        related_name='topics', 
        verbose_name='курс'
    )
    title = models.CharField(max_length=200, verbose_name='название темы')
    content = models.TextField(verbose_name='содержание темы')
    order = models.PositiveIntegerField(default=0, verbose_name='порядок')
    hours = models.PositiveIntegerField(default=2, verbose_name='часы')
    tests_count = models.PositiveIntegerField(default=0, verbose_name='количество тестов')
    assignments_count = models.PositiveIntegerField(default=1, verbose_name='количество заданий')
    info_blocks = models.PositiveIntegerField(default=0, verbose_name='блоки информации')
    is_completed = models.BooleanField(default=False, verbose_name='пройдено')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата обновления')
    
    ordering_number = models.PositiveIntegerField(
        default=0,
        verbose_name='порядковый номер'
    )
    duration = models.PositiveIntegerField(
        default=0,
        verbose_name='количество часов'
    )
    discipline = models.ForeignKey(
        'Discipline',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='дисциплина',
        related_name='topics'
    )

    class Meta:
        verbose_name = 'Учебная тема'
        verbose_name_plural = 'Учебные темы'
        ordering = ['discipline__title', 'ordering_number', 'order']
        unique_together = [['ordering_number', 'discipline']]

    def __str__(self):
        return self.title


class ControlPoint(models.Model):
    """Контрольная точка"""
    STATUS_CHOICES = [
        ('not_started', 'Не начато'),
        ('in_progress', 'В процессе'),
        ('submitted', 'На проверке'),
        ('passed', 'Сдано'),
    ]
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='control_points', verbose_name='тема')
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(verbose_name='описание задания')
    max_score = models.PositiveIntegerField(default=10, verbose_name='максимальный балл')
    student_score = models.PositiveIntegerField(default=0, verbose_name='полученный балл')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started', verbose_name='статус')
    order = models.PositiveIntegerField(default=0, verbose_name='порядок')

    class Meta:
        verbose_name = 'Контрольная точка'
        verbose_name_plural = 'Контрольные точки'
        ordering = ['order']

    def __str__(self):
        return self.title
from django.db import models
from django.conf import settings


class Group(models.Model):
    COURSE_CHOICES = [
        ('1', '1 курс'),
        ('2', '2 курс'),
        ('3', '3 курс'),
        ('4', '4 курс'),
    ]

    name = models.CharField(
        max_length=15,
        unique=True,
        verbose_name='название группы'
    )
    course = models.CharField(
        max_length=1,
        choices=COURSE_CHOICES,
        verbose_name='курс'
    )

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'
        ordering = ['course']
        indexes = [
            models.Index(fields=['course']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_course_display()})"


class Student(models.Model):
    last_name = models.CharField(
        max_length=40,
        verbose_name='фамилия'
    )
    first_name = models.CharField(
        max_length=20,
        verbose_name='имя'
    )
    patronymic = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name='отчество'
    )
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='аккаунт',
        related_name='student_profile'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='учебная группа',
        related_name='students'
    )

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['last_name', 'first_name']

    @property
    def full_name(self):
        parts = [self.last_name, self.first_name]
        if self.patronymic:
            parts.append(self.patronymic)
        return ' '.join(parts)

    def __str__(self):
        return self.full_name


class Discipline(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='название дисциплины'
    )
    duration = models.PositiveIntegerField(
        verbose_name='длительность (в часах)'
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
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.title


class Course(models.Model):
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
        verbose_name='дисциплина',
        related_name='courses'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='учебная группа',
        related_name='courses'
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='преподаватель',
        related_name='taught_courses',
        limit_choices_to={'is_staff': True}
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['discipline__title']
        indexes = [
            models.Index(fields=['discipline']),
            models.Index(fields=['group']),
            models.Index(fields=['teacher']),
        ]

    def __str__(self):
        return f"{self.discipline.title} - {self.group.name}"
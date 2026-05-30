from django.db import models
from django.conf import settings

class Group(models.Model):
    COURSE_CHOICES = [
        (1, '1 курс'),
        (2, '2 курс'),
        (3, '3 курс'),
        (4, '4 курс'),
    ]
    
    name = models.CharField(
        max_length=15, 
        unique=True,
        verbose_name='название группы'
    )
    course = models.IntegerField(
        choices=COURSE_CHOICES,
        verbose_name='курс'
    )
    
    class Meta:
        verbose_name = 'учебная группа'
        verbose_name_plural = 'учебные группы'
        ordering = ['course', 'name']
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
        related_name='student_profile',
        verbose_name='аккаунт'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name='учебная группа'
    )
    
    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'студенты'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    @property
    def full_name(self):
        if self.patronymic:
            return f"{self.last_name} {self.first_name} {self.patronymic}"
        return f"{self.last_name} {self.first_name}"
    
    @property
    def initials(self):
        if self.patronymic:
            return f"{self.last_name} {self.first_name[0]}.{self.patronymic[0]}."
        return f"{self.last_name} {self.first_name[0]}."
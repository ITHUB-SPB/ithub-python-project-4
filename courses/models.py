from django.db import models

from staff.models import Teacher
from students.models import Group

# Create your models here.
class Discipline(models.Model):
    title = models.CharField(max_length=50, null=False, verbose_name='Название')
    duration = models.PositiveBigIntegerField(null=False, verbose_name='Продолжительность')
    curriculum = models.FileField(null=True, verbose_name="Учебный план", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
        ordering = ['updated_at', 'created_at']

class Course(models.Model):
    code = models.CharField(max_length=15, null=False, verbose_name='Код')
    about = models.CharField(max_length=200, null=True, blank=True, verbose_name="О курсе")
    course_start = models.DateField(null=True, blank=True, verbose_name="Начало учебного периода")
    course_end = models.DateField(null=True, blank=True, verbose_name="Конец учебного периода")
    discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True, verbose_name="Дисциплина")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, verbose_name="Группа")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, verbose_name="Преподаватель")

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['code']


from django.db import models
from students.models import Group
from staff.models import Teacher

class Discipline(models.Model):
    title = models.CharField(max_length=50, null=False)
    duration = models.PositiveIntegerField(null=False, verbose_name='длительность')

    def __str__(self):
        return f'{self.title} ({self.duration} ак.ч.)'

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'


class Course(models.Model):
    code = models.CharField(max_length=15, unique=False, null=False)
    discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, related_name='students_group')


class Topic(models.Model):
    title = models.CharField(max_length=50, null=False)
    content = models.TextField(null=False)
    duration = models.PositiveIntegerField(null=False, verbose_name='длительность')

    discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ['discipline__title', 'title']

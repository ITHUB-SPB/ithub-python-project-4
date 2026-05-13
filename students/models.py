from django.contrib.auth import get_user_model
from django.db import models


class Course(models.TextChoices):
    first = '1', 'I'
    second = '2', 'II'
    third = '3', 'III'
    fourth = '4', 'IV'


class Group(models.Model):
    title = models.CharField(max_length=15, unique=True, null=False)
    course = models.CharField(choices=Course, null=False, verbose_name='Курс')

    def __str__(self):
        return f'{self.title} ({self.course})'


class Student(models.Model):
    account = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=40, null=False)
    last_name = models.CharField(max_length=40, null=False, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.group.title})'

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
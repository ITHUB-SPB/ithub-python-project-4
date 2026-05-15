from django.contrib.auth import get_user_model
from django.db import models


class Group(models.Model):
    class Course(models.TextChoices):
        first = 'first', 'I'
        second = 'second', 'II'
        third = 'third', 'III'
        fourth = 'fourth', 'IV'

    title = models.CharField(max_length=10, unique=True, null=False)
    course = models.CharField(choices=Course, null=False)

    def __str__(self):
        return self.title


class Student(models.Model):
    account = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=False)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    middle_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='Отчество')

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name or ""}'

    def get_initials(self):
        if self.middle_name:
            return f'{self.last_name} {str(self.first_name)[0]}.{str(self.middle_name)}.'
        return f'{self.last_name} {str(self.first_name)[0]}.'

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
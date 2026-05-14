from django.contrib.auth import get_user_model
from django.db import models


class Group(models.Model):
    class Courses(models.TextChoices):
        first = 'first', 'I'
        second = 'second', 'II'
        third = 'third', 'III'
        fourth = 'fourth', 'IV'

    title = models.CharField(max_length=10, null=False, unique=True)
    course = models.CharField(choices=Courses, null=False)

    def __str__(self):
        return self.title


class Student(models.Model):
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=30, null=False)
    middle_name = models.CharField(max_length=30, null=True, blank=True)

    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        related_name='students'
    )

    account = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.last_name} {str(self.first_name)[0]}.{str(self.middle_name)[0]}'
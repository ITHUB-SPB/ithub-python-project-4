from django.db import models


class Group(models.Model):
    class Course(models.TextChoices):
        first = 'first', 'I'
        second = 'second', 'II'
        third = 'third', 'III'
        fourth = 'fourth', 'IV'

    title = models.CharField(max_length=10, unique=True, null=False)
    course = models.CharField(choices=Course, null=False)

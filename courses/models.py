from django.db import models
from students.models import Group, Student

class Disclipline(models.Model):
    title = models.CharField(max_length=50, null=False)
    duration = models.PositiveIntegerField(null=False, verbose_name='Продолжительность')
    curriculum = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} ({self.duration} ак.ч.)'


class Course(models.Model):
    code = models.CharField(max_length=15, null=False, unique=True)
    discipline = models.ForeignKey(Disclipline, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_group')

    objects = models.Manager()


class Topic(models.Model):
    title = models.CharField(max_length=50, null=False)
    content = models.TextField(null=False)
    discipline = models.ForeignKey(Disclipline, on_delete=models.SET_NULL, null=True, blank=True)


class Assignment(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    weight = models.PositiveIntegerField(null=False)


class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    answer = models.TextField(null=False)
    score = models.PositiveIntegerField(null=False)
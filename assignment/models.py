from django.db import models
from courses.models import Topic
from students.models import Student

class Assignment(models.Model):
    weight = models.PositiveIntegerField(null=False, verbose_name='кол-во баллов')
    topic = models.OneToOneField(Topic, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateField(auto_now=True)


class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    answer = models.TextField(null=False)
    score = models.PositiveIntegerField(null=False, default=0)
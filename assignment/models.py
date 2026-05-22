from django.db import models
from courses.models import Discipline


class Assignment(models.Model):
    title = models.CharField(max_length=50, null=False)
    content = models.TextField(null=False)
    weight = models.PositiveIntegerField(null=False, verbose_name='кол-во баллов')
    discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateField(auto_now=True)

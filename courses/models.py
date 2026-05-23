from django.db import models
from students.models import Group
from staff.models import Teacher


class Discipline(models.Model):
	title = models.CharField(max_length=50, null=False)
	duration = models.PositiveSmallIntegerField(null=False, verbose_name='Длительность')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.title} ({self.duration} ак.ч.)'

	class Meta:
		verbose_name = 'Дисциплина'
		verbose_name_plural = 'Дисциплины'


class Course(models.Model):
	code = models.CharField(max_length=15, null=False)
	about = models.CharField(max_length=200, null=True, blank=True)
	discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True)
	group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
	teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
from django.contrib.auth import get_user_model
from django.db import models


class Group(models.Model):
	class Year(models.TextChoices):
		first = 'first', 'I'
		second = 'second', 'II'
		third = 'third', 'III'
		fourth = 'fourth', 'IV'

	title = models.CharField(max_length=10, null=False, unique=True)
	year = models.CharField(choices=Year, null=False)

	class Meta:
		ordering = ['year', '-title']
		indexes = [
			models.Index(fields=['year'])
		]


class Student(models.Model):
	first_name = models.CharField(max_length=20, null=False)
	last_name = models.CharField(max_length=40, null=False)
	middle_name = models.CharField(max_length=20, null=True, blank=True)
	account = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=False)
	group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return f'{self.last_name} {str(self.first_name)[0]} {str(self.middle_name)[0]}'
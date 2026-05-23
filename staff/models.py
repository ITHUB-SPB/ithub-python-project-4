from django.contrib.auth import get_user_model
from django.db import models


class Teacher(models.Model):
	first_name = models.CharField(max_length=20, null=False)
	last_name = models.CharField(max_length=40, null=False)
	middle_name = models.CharField(max_length=20, null=True, blank=True)
	account = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=False)

	def __str__(self):
		return f'{self.last_name} {str(self.first_name)[0]} {str(self.middle_name)[0]}'
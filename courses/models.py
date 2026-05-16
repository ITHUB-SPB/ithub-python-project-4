from django.db import models

class Discipline(models.Model):
	code = models.CharField(max_length=15, unique=True, null=False)
	title = models.CharField(max_length=50, null=False)
	duration = models.PositiveSmallIntegerField(null=False)
from django.db import models
from core import settings


class Teacher(models.Model):
    name = models.CharField("имя", max_length=20)
    surname = models.CharField("фамилия", max_length=40)
    lastname = models.CharField("отчество", max_length=40,null=True, blank=True)
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher",
        verbose_name="аккаунт"
    )

    def __str__(self):
        return f"{self.surname} {self.name} {self.lastname}"
    
class Manager(models.Model):
    name = models.CharField("имя", max_length=20)
    surname = models.CharField("фамилия", max_length=40)
    lastname = models.CharField("отчество", max_length=40,null=True, blank=True)
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="manager",
        verbose_name="аккаунт"
    )

    def __str__(self):
        return f"{self.surname} {self.name} {self.lastname}"
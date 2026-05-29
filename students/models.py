from django.db import models
from django.conf import settings

class Group(models.Model):
    class CourseChoice(models.TextChoices):
        first = "1 курс"
        second = "2 курс"
        third = "3 курс"
        fourth = "4 курс"

    title = models.CharField("номер", max_length=15)
    course = models.CharField("курс", max_length=10, choices=CourseChoice.choices)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        ordering = ["course"]


    def __str__(self):
        return f"{self.title} ({self.course})"

class Student(models.Model):
    name = models.CharField("имя", max_length=20)
    surname = models.CharField("фамилия", max_length=40)
    lastname = models.CharField("отчество", max_length=40,null=True, blank=True)
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student",
        verbose_name="аккаунт"
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
        verbose_name="группа"
        )
        
    
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ["surname", "name"]

    def __str__(self):
        return f"{self.surname} {self.name} {self.lastname}"



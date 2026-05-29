from django.db import models
from students.models import Group
from staff.models import Teacher

class Discipline(models.Model):
    title = models.CharField("название", max_length=50)
    duration = models.PositiveIntegerField("кол-во часов")
    curriculum = models.FileField("учебный план", upload_to="curriculums/", blank=True)
    created_at = models.DateTimeField("создано", auto_now_add=True)
    updated_at = models.DateTimeField("обновлено", auto_now=True)

    class Meta:
        verbose_name = "дисциплина"
        verbose_name_plural = "дисциплины"
        ordering = ["-updated_at", "-created_at"]



    def __str__(self):
        return self.title
    
class Course(models.Model):
    code = models.CharField("код", max_length=15)
    about = models.CharField("описание", max_length=200,blank=True)
    course_start = models.DateField("дата начала", null=True, blank=True)
    course_end = models.DateField("дата окончания", null=True, blank=True)
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        verbose_name="дисциплина"
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="группа"
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        verbose_name="преподаватель"
    )

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ["discipline__title"]
        indexes = [
            models.Index(fields=["discipline"]),
            models.Index(fields=["group"]),
            models.Index(fields=["teacher"])
        ]

    def __str__(self):
        return f"{self.code} - {self.discipline}" if self.discipline else self.code

class Topic(models.Model):
    title = models.CharField("название", max_length=50)
    content = models.TextField("содержание")
    order = models.PositiveIntegerField("порядок", default=0)
    discipline = models.ForeignKey(
        Discipline, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="topics",
        verbose_name="дисциплина"
    )

    class Meta:
        verbose_name = "топик"
        verbose_name_plural = "топики"
        ordering = ["order"]


    def __str__(self):
        return self.title
    
# class DisciplineTheme(models.Model):
#     title = models.CharField("тема", max_length=50)
#     order = models.PositiveIntegerField("порядок", default=0)
#     discipline = models.ForeignKey(
#         Discipline, 
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="theme",
#         verbose_name="дисциплина"
#     )
#     pass
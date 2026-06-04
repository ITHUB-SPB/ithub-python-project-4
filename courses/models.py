from django.db import models
from students.models import Group
from staff.models import Teacher

class Discipline(models.Model):
    title = models.CharField("Название дисциплины",max_length=50)
    duration = models.PositiveIntegerField("Длительность")
    curriculum = models.FileField("Учебный план", upload_to='curriculums/', blank=True, null=True)
    created_at = models.DateTimeField("Дата и время создания",auto_now_add=True)
    updated_at = models.DateTimeField("Дата и время последнего обновления",auto_now=True)

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"
        ordering = ['updated_at', 'created_at']

    def __str__(self):
        return self.title


class Course(models.Model):
    code = models.CharField("Код курса",max_length=15)
    about = models.CharField("Описание курса", max_length=200, blank=True, null=True)
    course_start = models.DateField("Дата начала", blank=True, null=True)
    course_end = models.DateField("Дата завершения",blank=True, null=True)

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.SET_NULL,
        null=True,
        related_name="courses",
        verbose_name="Дисциплина"
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Учебная группа"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        verbose_name="Преподаватель"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['code']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['discipline']),
            models.Index(fields=['group']),
        ]

    def __str__(self):
        return f"{self.code} ({self.discipline})"
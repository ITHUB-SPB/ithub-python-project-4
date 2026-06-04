from django.db import models
from students.models import Group
from staff.models import Teacher
from django.core.validators import MinValueValidator


class Discipline(models.Model):
    title = models.CharField("Название дисциплины", max_length=50)
    duration = models.PositiveIntegerField("Длительность")
    curriculum = models.FileField(
        "Учебный план", upload_to="curriculums/", blank=True, null=True
    )
    created_at = models.DateTimeField("Дата и время создания", auto_now_add=True)
    updated_at = models.DateTimeField(
        "Дата и время последнего обновления", auto_now=True
    )

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"
        ordering = ["updated_at", "created_at"]

    def __str__(self):
        return self.title


class Course(models.Model):
    code = models.CharField("Код курса", max_length=15)
    about = models.CharField("Описание курса", max_length=200, blank=True, null=True)
    course_start = models.DateField("Дата начала", blank=True, null=True)
    course_end = models.DateField("Дата завершения", blank=True, null=True)

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.SET_NULL,
        null=True,
        related_name="courses",
        verbose_name="Дисциплина",
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Учебная группа",
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        verbose_name="Преподаватель",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["code"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["discipline"]),
            models.Index(fields=["group"]),
        ]

    def __str__(self):
        return f"{self.code} ({self.discipline})"

    class Topic(models.Model):
        ordering_number = models.PositiveIntegerField(
            validators=[MinValueValidator(1)], verbose_name="Порядковый номер"
        )
        title = models.CharField(max_length=50, verbose_name="Название темы")
        content = models.TextField(verbose_name="Содержимое темы")
        duration = models.PositiveIntegerField(
            validators=[MinValueValidator(1)], verbose_name="Количество часов"
        )
        discipline = models.ForeignKey(
            "Discipline",
            on_delete=models.SET_NULL,
            null=True,
            verbose_name="Дисциплина",
        )

        class Meta:
            verbose_name = "Учебная тема"
            verbose_name_plural = "Учебные темы"
            ordering = ["discipline", "ordering_number"]
            unique_together = ("ordering_number", "discipline")

        def __str__(self):
            discipline_title = (
                self.discipline.title if self.discipline else "Без дисциплины"
            )
            return f"{self.ordering_number}. {self.title} ({discipline_title})"

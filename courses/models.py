from django.core.validators import MinValueValidator
from django.db import models


class Discipline(models.Model):
    title = models.CharField(max_length=50, verbose_name="название")
    duration = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="длительность")
    curriculum = models.FileField(upload_to="curriculums/", null=True, blank=True, verbose_name="учебный план")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлено")

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"
        ordering = ["-updated_at", "-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["updated_at", "created_at"]),
        ]

    def __str__(self):
        return self.title


class Course(models.Model):
    code = models.CharField(max_length=15, verbose_name="код")
    about = models.CharField(max_length=200, blank=True, verbose_name="описание")
    course_start = models.DateField(null=True, blank=True, verbose_name="начало курса")
    course_end = models.DateField(null=True, blank=True, verbose_name="конец курса")
    discipline = models.ForeignKey(
        "courses.Discipline",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        verbose_name="дисциплина",
    )
    group = models.ForeignKey(
        "students.Group",
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="группа",
    )
    teacher = models.ForeignKey(
        "staff.Teacher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        verbose_name="преподаватель",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["discipline_id", "code"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["discipline"]),
            models.Index(fields=["group"]),
            models.Index(fields=["teacher"]),
        ]

    def __str__(self):
        return self.code


class Topic(models.Model):
    ordering_number = models.PositiveIntegerField(verbose_name="порядковый номер")
    title = models.CharField(max_length=50, verbose_name="название")
    content = models.TextField(verbose_name="содержимое")
    duration = models.PositiveIntegerField(verbose_name="количество часов")
    discipline = models.ForeignKey(
        "courses.Discipline",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="topics",
        verbose_name="дисциплина",
    )

    class Meta:
        verbose_name = "Учебная тема"
        verbose_name_plural = "Учебные темы"
        ordering = ["discipline_id", "ordering_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["ordering_number", "discipline"],
                name="unique_topic_ordering_number_discipline",
            )
        ]
        indexes = [
            models.Index(fields=["discipline", "ordering_number"]),
        ]

    def __str__(self):
        return self.title

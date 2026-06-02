from django.core.validators import MinValueValidator
from django.db import models

from staff.models import Teacher
from students.models import Group, Student


class Discipline(models.Model):
    title = models.CharField(max_length=50, verbose_name="название")
    duration = models.PositiveIntegerField(validators=[MinValueValidator(0)], verbose_name="длительность")
    curriculum = models.FileField(upload_to="curricula/", blank=True, null=True, verbose_name="учебный план")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлено")

    class Meta:
        verbose_name = "дисциплина"
        verbose_name_plural = "дисциплины"
        ordering = ("-updated_at", "-created_at")
        indexes = [
            models.Index(fields=("title",)),
            models.Index(fields=("duration",)),
            models.Index(fields=("updated_at",)),
        ]

    def __str__(self):
        return self.title


class Course(models.Model):
    code = models.CharField(max_length=15, db_index=True, verbose_name="код")
    about = models.CharField(max_length=200, blank=True, verbose_name="описание")
    course_start = models.DateField(blank=True, null=True, verbose_name="дата начала")
    course_end = models.DateField(blank=True, null=True, verbose_name="дата окончания")
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        verbose_name="дисциплина",
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="courses", verbose_name="учебная группа")
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        verbose_name="преподаватель",
    )

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ("discipline__title", "code")
        indexes = [
            models.Index(fields=("code",)),
            models.Index(fields=("discipline",)),
            models.Index(fields=("group",)),
            models.Index(fields=("teacher",)),
            models.Index(fields=("course_start",)),
            models.Index(fields=("course_end",)),
        ]

    def __str__(self):
        discipline = self.discipline.title if self.discipline else "Без дисциплины"
        return f"{discipline} ({self.code})"


class Topic(models.Model):
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        related_name="topics",
        verbose_name="дисциплина",
    )
    title = models.CharField(max_length=150, verbose_name="название")
    study_hours = models.PositiveIntegerField(default=2, verbose_name="часы на изучение")
    order = models.PositiveIntegerField(default=1, verbose_name="порядок")
    goal = models.TextField(blank=True, verbose_name="зачем это учить")
    study_plan = models.TextField(blank=True, verbose_name="как это учить")
    content = models.TextField(blank=True, verbose_name="содержательная часть")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлено")

    class Meta:
        verbose_name = "учебная тема"
        verbose_name_plural = "учебные темы"
        ordering = ("order", "id")
        indexes = [
            models.Index(fields=("discipline", "order")),
            models.Index(fields=("title",)),
        ]

    def __str__(self):
        return self.title


class ControlPoint(models.Model):
    topic = models.OneToOneField(
        Topic,
        on_delete=models.CASCADE,
        related_name="control_point",
        verbose_name="тема",
    )
    title = models.CharField(max_length=150, verbose_name="название")
    task = models.TextField(verbose_name="задание")
    max_score = models.PositiveIntegerField(default=10, verbose_name="максимальный балл")

    class Meta:
        verbose_name = "контрольная точка"
        verbose_name_plural = "контрольные точки"
        ordering = ("topic__order", "id")
        indexes = [
            models.Index(fields=("topic",)),
            models.Index(fields=("max_score",)),
        ]

    def __str__(self):
        return self.title


class Submission(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="submissions", verbose_name="курс")
    control_point = models.ForeignKey(
        ControlPoint,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name="контрольная точка",
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="submissions", verbose_name="студент")
    message = models.TextField(blank=True, verbose_name="сообщение")
    attachment = models.FileField(upload_to="submissions/", blank=True, null=True, verbose_name="файл")
    score = models.PositiveIntegerField(blank=True, null=True, verbose_name="оценка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="отправлено")
    reviewed_at = models.DateTimeField(blank=True, null=True, verbose_name="проверено")

    class Meta:
        verbose_name = "ответ"
        verbose_name_plural = "ответы"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("course", "control_point", "student"),
                name="unique_submission_per_control_point",
            )
        ]
        indexes = [
            models.Index(fields=("course", "student")),
            models.Index(fields=("control_point",)),
            models.Index(fields=("score",)),
        ]

    def __str__(self):
        return f"{self.student.short_name} - {self.control_point.title}"

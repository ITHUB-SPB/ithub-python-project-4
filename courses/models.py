from django.db import models
from students.models import Group, Student
from staff.models import Teacher


class Discipline(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    duration = models.PositiveIntegerField(verbose_name="Длительность")
    curriculum = models.FileField(upload_to="curriculums/", null=True, blank=True, verbose_name="Учебный план")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"
        ordering = ["updated_at", "created_at"]
        indexes = [models.Index(fields=["updated_at", "created_at"])]

    def __str__(self):
        return self.title


class Course(models.Model):
    code = models.CharField(max_length=15, verbose_name="Код")
    about = models.CharField(max_length=200, null=True, blank=True, verbose_name="Описание")
    course_start = models.DateField(null=True, blank=True, verbose_name="Начало")
    course_end = models.DateField(null=True, blank=True, verbose_name="Конец")
    discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Дисциплина")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Преподаватель")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["discipline__title"]
        indexes = [models.Index(fields=["code"]), models.Index(fields=["discipline"]), models.Index(fields=["group"])]

    def __str__(self):
        return self.code


class Topic(models.Model):
    ordering_number = models.PositiveIntegerField(verbose_name="Номер")
    title = models.CharField(max_length=50, verbose_name="Название")
    content = models.TextField(verbose_name="Содержимое")
    duration = models.PositiveIntegerField(verbose_name="Часы")
    discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True, blank=True, related_name="topics", verbose_name="Дисциплина")

    class Meta:
        verbose_name = "Топик"
        verbose_name_plural = "Топики"
        ordering = ["discipline_id", "ordering_number"]
        constraints = [
            models.UniqueConstraint(fields=["ordering_number", "discipline"], name="unique_topic_number_in_discipline"),
        ]

    def __str__(self):
        return self.title


class Assignment(models.Model):
    topic = models.OneToOneField(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name="assignment", verbose_name="Топик")
    weight = models.PositiveIntegerField(verbose_name="Максимальный балл")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Контрольная точка"
        verbose_name_plural = "Контрольные точки"
        ordering = ["topic__discipline_id", "topic__ordering_number"]

    def __str__(self):
        if self.topic:
            return self.topic.title
        return f"Контрольная точка {self.pk}"


class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="submissions", verbose_name="Студент")
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions", verbose_name="Контрольная точка")
    answer = models.TextField(verbose_name="Ответ")
    score = models.PositiveIntegerField(null=True, blank=True, verbose_name="Оценка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        ordering = ["assignment__topic__discipline_id", "assignment__topic__ordering_number"]

    def save(self, *args, **kwargs):
        if self.score is not None and self.assignment_id and self.score > self.assignment.weight:
            self.score = self.assignment.weight
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.assignment}"

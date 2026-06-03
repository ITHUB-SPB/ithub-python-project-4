from django.core.exceptions import ValidationError
from django.db import models


class Assignment(models.Model):
    topic = models.OneToOneField(
        "courses.Topic",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assignment",
        verbose_name="топик",
    )
    weight = models.PositiveIntegerField(verbose_name="максимальный балл")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлено")

    class Meta:
        verbose_name = "Контрольная точка"
        verbose_name_plural = "Контрольные точки"
        ordering = ["topic__discipline_id", "topic__ordering_number"]

    def __str__(self):
        if self.topic:
            return f"{self.topic.title}"
        return f"Контрольная точка {self.pk}"


class Submission(models.Model):
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name="студент",
    )
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name="контрольная точка",
    )
    answer = models.TextField(verbose_name="ответ")
    score = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="оценка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлено")

    class Meta:
        verbose_name = "Ответ на контрольную точку"
        verbose_name_plural = "Ответы на контрольные точки"
        ordering = ["assignment__topic__discipline_id", "assignment__topic__ordering_number"]
        constraints = [
            models.UniqueConstraint(fields=["student", "assignment"], name="unique_student_assignment"),
        ]

    def clean(self):
        if self.score is not None and self.assignment and self.score > self.assignment.weight:
            raise ValidationError({"score": "Оценка не может быть больше максимального балла"})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.assignment}"

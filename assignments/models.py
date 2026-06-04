from django.core.exceptions import ValidationError
from django.db import models

from courses.models import Topic
from students.models import Student


class Assignment(models.Model):
    topic = models.OneToOneField(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assignment",
        verbose_name="тема",
    )
    weight = models.PositiveIntegerField(verbose_name="максимальный балл")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлено")

    class Meta:
        verbose_name = "контрольная точка"
        verbose_name_plural = "контрольные точки"
        ordering = ["topic__discipline", "topic__ordering_number"]

    def __str__(self):
        return f"{self.topic}"


class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="submissions", verbose_name="студент")
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name="контрольная точка",
    )
    answer = models.TextField(verbose_name="ответ")
    score = models.PositiveIntegerField(null=True, blank=True, verbose_name="оценка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлено")

    class Meta:
        verbose_name = "ответ"
        verbose_name_plural = "ответы"
        ordering = ["assignment__topic__discipline", "assignment__topic__ordering_number"]
        constraints = [models.UniqueConstraint(fields=["student", "assignment"], name="unique_submission")]

    def clean(self):
        if self.score is not None and self.assignment_id and self.score > self.assignment.weight:
            raise ValidationError({"score": "Оценка не может быть больше максимального балла"})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.assignment}"

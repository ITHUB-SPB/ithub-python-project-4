from django.db import models
from django.core.exceptions import ValidationError
from content.models import Topic
from students.models import Student


class Assignment(models.Model):
    topic = models.OneToOneField(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='тема',
        related_name='assignment'
    )
    weight = models.PositiveIntegerField(
        verbose_name='максимальный балл'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='дата обновления'
    )

    class Meta:
        verbose_name = 'Контрольная точка'
        verbose_name_plural = 'Контрольные точки'
        ordering = ['topic__discipline', 'topic__ordering_number']

    def __str__(self):
        return f"КТ: {self.topic.title} (макс. {self.weight} баллов)"


class Submission(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='студент',
        related_name='submissions'
    )
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        verbose_name='контрольная точка',
        related_name='submissions'
    )
    score = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name='оценка'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='дата обновления'
    )

    class Meta:
        verbose_name = 'Ответ на контрольную точку'
        verbose_name_plural = 'Ответы на контрольные точки'
        ordering = ['assignment__topic__discipline', 'assignment__topic__ordering_number']
        unique_together = [['student', 'assignment']]  # один студент — один ответ на КТ

    def clean(self):
        if self.score and self.assignment and self.score > self.assignment.weight:
            raise ValidationError(f'Оценка не может превышать {self.assignment.weight} баллов')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        status = f"{self.score}/{self.assignment.weight}" if self.score is not None else "На проверке"
        return f"{self.student.full_name} - {self.assignment.topic.title}: {status}"
from django.db import models
from django.core.exceptions import ValidationError
from courses.models import Topic
from students.models import Student


class Assignment(models.Model):
    """Контрольная точка"""
    topic = models.OneToOneField(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='топик',
        related_name='assignment'
    )
    weight = models.PositiveIntegerField(
        default=10,
        verbose_name='максимальный балл'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='дата последнего обновления'
    )

    class Meta:
        verbose_name = 'Контрольная точка'
        verbose_name_plural = 'Контрольные точки'
        ordering = ['topic__discipline__title', 'topic__ordering_number']

    def __str__(self):
        topic_title = self.topic.title if self.topic else 'Без топика'
        return f"КТ: {topic_title} ({self.weight} баллов)"


class Submission(models.Model):
    """Ответ на контрольную точку"""
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
    answer = models.TextField(
        verbose_name='ответ'
    )
    score = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=0,
        verbose_name='оценка'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='дата последнего обновления'
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['-created_at']

    def clean(self):
        if self.score and self.assignment and self.score > self.assignment.weight:
            raise ValidationError(
                f'Оценка ({self.score}) не может превышать '
                f'максимальный балл ({self.assignment.weight})'
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        score_display = self.score if self.score is not None else 'На проверке'
        return f"{self.student} - {self.assignment}: {score_display}"
from django.db import models
from django.core.exceptions import ValidationError
from courses.models import Topic
from students.models import Student

class Assignment(models.Model):
    topic = models.OneToOneField(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assignment',
        verbose_name='тема'
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
        verbose_name = 'контрольная точка'
        verbose_name_plural = 'контрольные точки'
        ordering = ['topic__discipline__code', 'topic__ordering_number']
    
    def __str__(self):
        return f"КТ: {self.topic.title if self.topic else 'Без темы'}"


class Submission(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='студент'
    )
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='контрольная точка'
    )
    answer = models.TextField(
        verbose_name='ответ'
    )
    score = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='оценка'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата отправки'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='дата обновления'
    )
    
    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'
        ordering = ['-created_at']
        unique_together = [['student', 'assignment']]
    
    def clean(self):
        if self.score is not None and self.assignment:
            if self.score > self.assignment.weight:
                raise ValidationError(
                    f'Оценка не может превышать максимальный балл ({self.assignment.weight})'
                )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        status = f"{self.score}/{self.assignment.weight}" if self.score is not None else "На проверке"
        return f"{self.student} - {self.assignment} - {status}"
from django.db import models
from django.core.exceptions import ValidationError


class Assignment(models.Model):
    topic = models.OneToOneField(
        'courses.Topic',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assignment',
        verbose_name='топик'
    )

    weight = models.PositiveIntegerField(
        verbose_name='максимальный балл'
    )

    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name='дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='дата обновления'
    )

    class Meta:
        verbose_name = 'контрольная точка'
        verbose_name_plural = 'контрольные точки'
        ordering = ['topic__discipline', 'topic__ordering_number']

    def __str__(self):
        return f'КТ: {self.topic.title}' if self.topic else f'КТ #{self.pk}'


class Submission(models.Model):
    student = models.ForeignKey(
        'students.Student',
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
        default=0,
        verbose_name='оценка'
    )

    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name='дата создания'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='дата обновления'
    )

    class Meta:
        verbose_name = 'ответ на КТ'
        verbose_name_plural = 'ответы на КТ'
        ordering = ['assignment__topic__discipline', 'assignment__topic__ordering_number']

    def __str__(self):
        return f'{self.student}: {self.assignment}'

    def clean(self):
        if self.score and self.assignment and self.score > self.assignment.weight:
            raise ValidationError({
                'score': f'Оценка не может превышать максимальный балл ({self.assignment.weight})'
            })

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
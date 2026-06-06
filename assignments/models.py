from django.db import models
from django.core.exceptions import ValidationError


class Assignment(models.Model):
    topic = models.OneToOneField('courses.Topic', on_delete=models.SET_NULL, null=True, verbose_name='Тема')
    weight = models.PositiveIntegerField(verbose_name='Максимальный балл')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Контрольная точка'
        verbose_name_plural = 'Контрольные точки'

        ordering = [
            'topic__discipline',
            'topic__ordering_number',
        ]

    def __str__(self):
        return f'{self.topic} ({self.weight} баллов)'

class Submission(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, verbose_name='Студент')

    assignment = models.ForeignKey('assignments.Assignment', on_delete=models.CASCADE, verbose_name='Контрольная точка')
    answer = models.TextField(verbose_name='Ответ')
    score = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='Оценка')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Ответ на контрольную точку'
        verbose_name_plural = 'Ответы на контрольные точки'

        ordering = [
            'assignment__topic__discipline',
            'assignment__topic__ordering_number',
        ]

    def clean(self):
        if (
            self.score is not None
            and self.assignment
            and self.score > self.assignment.weight
        ):
            raise ValidationError({
                'score': (
                    f'Оценка не может превышать '
                    f'{self.assignment.weight}'
                )
            })

    def __str__(self):
        return (
            f'{self.student} - '
            f'{self.assignment}'
        )
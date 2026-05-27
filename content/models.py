from django.db import models
from students.models import Discipline


class Topic(models.Model):
    ordering_number = models.PositiveIntegerField(
        verbose_name='порядковый номер'
    )
    title = models.CharField(
        max_length=50,
        verbose_name='название темы'
    )
    content = models.TextField(
        verbose_name='содержание'
    )
    duration = models.PositiveIntegerField(
        verbose_name='количество часов'
    )
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='дисциплина',
        related_name='topics'
    )

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ['discipline', 'ordering_number']
        unique_together = [['ordering_number', 'discipline']]

    def __str__(self):
        return f"{self.discipline.title} - {self.ordering_number}. {self.title}"
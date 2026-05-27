from django.db import models
from students.models import Course


class Topic(models.Model):
    TYPE_CHOICES = [
        ('material', 'Учебный материал'),
        ('checkpoint', 'Контрольная точка'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name='название'
    )
    content = models.TextField(
        verbose_name='содержание'
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name='тип'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='курс',
        related_name='topics'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='порядковый номер'
    )

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ['course', 'order', 'id']

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"
from django.db import models

class Discipline(models.Model):
    code = models.CharField(max_length=15, unique=True, null=False)
    title = models.CharField(max_length=50, null=False)
    duration = models.PositiveIntegerField(null=False, verbose_name='длительность')

    def __str__(self):
        return f'{self.code} {self.title} ({self.duration} ак.ч.)'

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
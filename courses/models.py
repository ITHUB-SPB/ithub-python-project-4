from django.db import models

class Disclipline(models.Model):
    code = models.CharField(max_length=15, null=False, unique=True)
    title = models.CharField(max_length=50, null=False)
    duration = models.PositiveIntegerField(null=False, verbose_name='Продолжительность')

    def __str__(self):
        return f'{self.code} {self.title} ({self.duration} ак.ч.)'
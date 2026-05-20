from django.contrib.auth import get_user_model
from django.db import models


class Staff(models.Model):
    account = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40, null=False)
    last_name = models.CharField(max_length=40, null=False, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
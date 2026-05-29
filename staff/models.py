from django.contrib.auth import get_user_model
from django.db import models


class Teacher(models.Model):
    account = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=False)

    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    middle_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='Отчество')

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name or ""}'

    def get_initials(self):
        if self.middle_name:
            return f'{self.last_name} {str(self.first_name)[0]}.{str(self.middle_name)}.'
        return f'{self.last_name} {str(self.first_name)[0]}.'

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
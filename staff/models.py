from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Teacher(models.Model):
    first_name = models.CharField(max_length=20, null=False, verbose_name="Имя")
    last_name = models.CharField(max_length=40, null=False, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=40, null=True, blank=True, verbose_name="Отчество")
    account = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=False, verbose_name="Аккаунт")

    def __str__(self):
        return f'{self.first_name} {self.last_name} {str(self.middle_name) [0]}'
    
    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        ordering = ['last_name', 'first_name']
    
class Manager(models.Model):
    first_name = models.CharField(max_length=20, null=False, verbose_name="Имя")
    last_name = models.CharField(max_length=40, null=False, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=40, null=True, blank=True, verbose_name="Отчество")
    account = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=False, verbose_name="Аккаунт")

    def __str__(self):
        return f'{self.first_name} {self.last_name} {str(self.middle_name) [0]}'
    
    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'
        ordering = ['last_name', 'first_name']

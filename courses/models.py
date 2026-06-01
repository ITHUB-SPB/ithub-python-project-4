from django.db import models

from staff.models import Teacher
from students.models import Group, Student

# Create your models here.
class Discipline(models.Model):
    title = models.CharField(max_length=50, null=False, verbose_name='Название')
    duration = models.PositiveBigIntegerField(null=False, verbose_name='Продолжительность')
    curriculum = models.FileField(null=True, verbose_name="Учебный план", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
        ordering = ['-updated_at', '-created_at']

class Course(models.Model):
    code = models.CharField(max_length=15, null=False, verbose_name='Код')
    about = models.CharField(max_length=200, null=True, blank=True, verbose_name="О курсе")
    course_start = models.DateField(null=True, blank=True, verbose_name="Начало учебного периода")
    course_end = models.DateField(null=True, blank=True, verbose_name="Конец учебного периода")
    discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True, verbose_name="Дисциплина")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, verbose_name="Группа")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, verbose_name="Преподаватель")

    def __str__(self):
        return f'{self.discipline.title} - {self.group.title}'
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['code']

    

class Topic(models.Model):
    orderingnumber = models.PositiveIntegerField(null=False, verbose_name='Порядковый номер')
    title = models.CharField(max_length=50, null=False, verbose_name='Название')
    content = models.TextField(null=True, blank=True, verbose_name="Содержание")
    duration = models.PositiveBigIntegerField(null=False, verbose_name='Продолжительность')
    discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True, verbose_name="Дисциплина")
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ['discipline', 'orderingnumber']
        constraints = [
             models.UniqueConstraint(fields=['discipline', 'orderingnumber'], name='orderingnumber_per_discipline')
        ]

class Assignment(models.Model):
    topic = models.OneToOneField(Topic, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Тема")
    weight = models.PositiveIntegerField(null=False, verbose_name='Вес задания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление")
    content = models.TextField(null=True, blank=True, verbose_name="Содержание")
    

    def __str__(self):
        return f'Задание для темы: {self.topic.title}'
    
    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['topic__discipline', 'topic__orderingnumber']

class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False, verbose_name="Студент")
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=False, verbose_name="Задание")
    answer = models.TextField(null=False, blank=False, verbose_name="Ответ")
    score = models.PositiveIntegerField(null=True, default=0, verbose_name="Оценка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление")

    def __str__(self):
        return f'Ответ студента {self.student.last_name} {self.student.first_name} на задание {self.assignment.topic.title}'
    
    def save(self, *args, **kwargs):
        if self.score is None or self.score == 0:
            self.score = 0
            super().save(*args, **kwargs) 
        if self.score > self.assignment.weight:
            raise ValueError("Оценка не может превышать максимумальный балл")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ответ студента'
        verbose_name_plural = 'Ответы студентов'
        ordering = ['assignment__topic__discipline']
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'assignment'],
                name='unique_student_assignment'
            )
        ]
    
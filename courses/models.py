from django.db import models

class Discipline(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')

    duration = models.PositiveIntegerField(verbose_name='Длительность')
    curriculum = models.FileField(upload_to='curriculums/', null=True, blank=True, verbose_name='Учебный план')

    created_at = models.DateTimeField( auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField( auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
        ordering = ['-updated_at', '-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['updated_at']),
        ]


class Course(models.Model):
    code = models.CharField(max_length=15, verbose_name='Код курса')

    about = models.CharField( max_length=200, null=True, blank=True, verbose_name='Описание')

    course_start = models.DateField(null=True, blank=True, verbose_name='Дата начала')
    course_end = models.DateField(null=True, blank=True, verbose_name='Дата окончания')

    discipline = models.ForeignKey('courses.Discipline', on_delete=models.SET_NULL, null=True, verbose_name='Дисциплина')
    group = models.ForeignKey('students.Group', on_delete=models.CASCADE, related_name='courses', verbose_name='Группа')
    teacher = models.ForeignKey('staff.Teacher', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Преподаватель')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['discipline__title']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['course_start']),
        ]
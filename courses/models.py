from django.db import models
from staff.models import Staff


class Discipline(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    code = models.CharField(max_length=15, unique=True, null=False, blank=False, verbose_name="Код "
                                                                                              "дисциплины")
    duration = models.PositiveIntegerField()
    curriculum = models.FileField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Course(models.Model):
    about = models.TextField(null=False, blank=False)

    course_start = models.DateField(null=True)
    course_end = models.DateField(null=True)

    discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        code = self.discipline.code if self.discipline else ''
        title = self.discipline.title if self.discipline else ''
        teacher = self.teacher.lastname if self.teacher else ''

        return f'{code} «{title}» ({teacher})'
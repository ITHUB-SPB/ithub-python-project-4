from django.db import models
from staff.models import Staff
from students.models import Group, Student


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
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, related_name='learning_course')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        code = self.discipline.code if self.discipline else ''
        title = self.discipline.title if self.discipline else ''
        teacher = self.teacher or ''

        return f'{code} «{title}» ({self.group}, {teacher})'


class Topic(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True, blank=True)


class Assignment(models.Model):
    topic = models.OneToOneField(Topic, on_delete=models.CASCADE)
    weight = models.PositiveIntegerField(null=False)


class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    answer = models.TextField(null=False)
    score = models.PositiveIntegerField(null=True, blank=True, default=0)
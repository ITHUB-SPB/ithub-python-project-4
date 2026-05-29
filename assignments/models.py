from django.db import models
from courses.models import Discipline
from students.models import Student

class Assignment(models.Model):
    title = models.CharField("название", max_length=50)
    content = models.TextField("содержание")
    order = models.PositiveIntegerField("порядок", default=0)
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assignments",
        verbose_name="дисциплина"
    )
    weight = models.PositiveIntegerField("макс баллов")

    class Meta:
        verbose_name = "контрольная точка"
        verbose_name_plural = "контрольные точки"
        ordering = ["order"]

    def __str__(self):
        return self.title

class Answer(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="студент"
    )
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="задание"
    )
    value = models.TextField("ответ")
    score = models.PositiveIntegerField("оценка", null=True, blank=True)

    class Meta:
        verbose_name = "ответ"
        verbose_name_plural = "ответы"
        unique_together = ("student", "assignment")

    def __str__(self):
        return f"{self.student} - {self.assignment}"
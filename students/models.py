from django.conf import settings
from django.db import models


class Group(models.Model):
    COURSE_1 = "1"
    COURSE_2 = "2"
    COURSE_3 = "3"
    COURSE_4 = "4"
    COURSE_CHOICES = [
        (COURSE_1, "1 курс"),
        (COURSE_2, "2 курс"),
        (COURSE_3, "3 курс"),
        (COURSE_4, "4 курс"),
    ]

    title = models.CharField(max_length=15, verbose_name="название")
    course = models.CharField(max_length=1, choices=COURSE_CHOICES, verbose_name="курс")

    class Meta:
        verbose_name = "учебная группа"
        verbose_name_plural = "учебные группы"
        ordering = ["course", "title"]
        indexes = [models.Index(fields=["course"])]

    def __str__(self):
        return f"{self.title} ({self.get_course_display()})"


class Student(models.Model):
    first_name = models.CharField(max_length=20, verbose_name="имя")
    last_name = models.CharField(max_length=40, verbose_name="фамилия")
    middle_name = models.CharField(max_length=40, blank=True, verbose_name="отчество")
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student",
        verbose_name="аккаунт",
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
        verbose_name="группа",
    )

    class Meta:
        verbose_name = "студент"
        verbose_name_plural = "студенты"
        ordering = ["last_name", "first_name"]
        indexes = [models.Index(fields=["last_name", "first_name"])]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def short_name(self):
        initials = self.first_name[:1]
        if self.middle_name:
            initials += f".{self.middle_name[:1]}"
        return f"{self.last_name} {initials}."

from django.conf import settings
from django.db import models


class Group(models.Model):
    class CourseChoices(models.TextChoices):
        FIRST = "1", "1 курс"
        SECOND = "2", "2 курс"
        THIRD = "3", "3 курс"
        FOURTH = "4", "4 курс"

    name = models.CharField(max_length=15, verbose_name="название")
    course = models.CharField(max_length=1, choices=CourseChoices.choices, db_index=True, verbose_name="курс")

    class Meta:
        verbose_name = "учебная группа"
        verbose_name_plural = "учебные группы"
        ordering = ("course", "name")
        indexes = [models.Index(fields=("course",))]

    def __str__(self):
        return self.name


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
        verbose_name="учебная группа",
    )

    class Meta:
        verbose_name = "студент"
        verbose_name_plural = "студенты"
        ordering = ("last_name", "first_name")
        indexes = [
            models.Index(fields=("last_name", "first_name")),
            models.Index(fields=("group",)),
        ]

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        parts = [self.last_name, self.first_name, self.middle_name]
        return " ".join(part for part in parts if part)

    @property
    def initials(self):
        letters = [self.first_name[:1], self.last_name[:1]]
        return "".join(letter.upper() for letter in letters if letter)

    @property
    def short_name(self):
        first = f"{self.first_name[:1]}." if self.first_name else ""
        middle = f"{self.middle_name[:1]}." if self.middle_name else ""
        return f"{self.last_name} {first}{middle}".strip()

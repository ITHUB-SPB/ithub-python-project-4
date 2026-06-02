from django.conf import settings
from django.db import models


class EmployeeBase(models.Model):
    first_name = models.CharField(max_length=20, verbose_name="имя")
    last_name = models.CharField(max_length=40, verbose_name="фамилия")
    middle_name = models.CharField(max_length=40, blank=True, verbose_name="отчество")
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="аккаунт",
    )

    class Meta:
        abstract = True
        ordering = ("-last_name", "-first_name", "-middle_name")

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


class Teacher(EmployeeBase):
    class Meta(EmployeeBase.Meta):
        verbose_name = "преподаватель"
        verbose_name_plural = "преподаватели"


class Manager(EmployeeBase):
    class Meta(EmployeeBase.Meta):
        verbose_name = "менеджер"
        verbose_name_plural = "менеджеры"

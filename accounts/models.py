from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, *, username, password, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        if not password:
            raise ValueError("Password is required")
        user = self.model(username=self.model.normalize_username(username), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username=username, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, verbose_name="логин")
    is_active = models.BooleanField(default=True, verbose_name="активен")
    is_staff = models.BooleanField(default=False, verbose_name="сотрудник")
    is_superuser = models.BooleanField(default=False, verbose_name="суперпользователь")

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "аккаунт"
        verbose_name_plural = "аккаунты"

    def __str__(self):
        if hasattr(self, "manager"):
            role = "менеджер"
        elif hasattr(self, "teacher"):
            role = "преподаватель"
        elif hasattr(self, "student"):
            role = "студент"
        elif self.is_superuser:
            role = "суперпользователь"
        elif self.is_staff:
            role = "сотрудник"
        else:
            role = "пользователь"
        return f"{self.username} ({role})"

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from students.models import Group

class UserManager(BaseUserManager):
    def create_user(self, *, username, password, **extra_fields):
        if not username:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")

        user = self.model(
            username=User.normalize_username(username),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(
            username=username,
            password=password,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, null=False, blank=False, verbose_name='логин')

    first_name = models.CharField(max_length=30, verbose_name='имя')
    last_name = models.CharField(max_length=30, verbose_name='фамилия')
    middle_name = models.CharField(max_length=30, verbose_name='отчество')

    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE, related_name='students', verbose_name='группа')

    is_staff = models.BooleanField(default=False, verbose_name='сотрудник')
    is_superuser = models.BooleanField(default=False, verbose_name='менеджер')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f'{self.username} ({self.last_name} {self.first_name})'

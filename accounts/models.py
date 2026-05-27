from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

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

    is_staff = models.BooleanField(default=False, verbose_name='сотрудник')
    is_superuser = models.BooleanField(default=False, verbose_name='менеджер')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    def __str__(self):
        role = 'суперадмин' if self.is_superuser else 'сотрудник' if self.is_staff else 'студент'
        return f'{self.username} ({role})'

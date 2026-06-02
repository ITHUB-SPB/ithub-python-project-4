from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, *, username, password, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        if not password:
            raise ValueError("Password is required")
        user = self.model(
            username=self.model.normalize_username(username),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(
            username=username,
            password=password,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, verbose_name="логин")
    is_staff = models.BooleanField(default=False, verbose_name="сотрудник")
    is_superuser = models.BooleanField(default=False, verbose_name="менеджер")

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "аккаунт"
        verbose_name_plural = "аккаунты"

    def __str__(self):
        return self.username

    @property
    def profile(self):
        for attr in ("student", "teacher", "manager"):
            try:
                profile = getattr(self, attr)
            except AttributeError:
                profile = None
            if profile is not None:
                return profile
        return None

    @property
    def display_name(self):
        profile = self.profile
        return profile.full_name if profile is not None else self.username

    @property
    def avatar_text(self):
        profile = self.profile
        if profile is None:
            return self.username[:2].upper()
        return profile.initials

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Teacher",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=20, verbose_name="имя")),
                ("last_name", models.CharField(max_length=40, verbose_name="фамилия")),
                ("patronymic", models.CharField(blank=True, max_length=40, verbose_name="отчество")),
                ("account", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="teacher", to=settings.AUTH_USER_MODEL, verbose_name="аккаунт")),
            ],
            options={
                "verbose_name": "Преподаватель",
                "verbose_name_plural": "Преподаватели",
                "ordering": ["last_name", "first_name", "patronymic"],
            },
        ),
        migrations.CreateModel(
            name="Manager",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=20, verbose_name="имя")),
                ("last_name", models.CharField(max_length=40, verbose_name="фамилия")),
                ("patronymic", models.CharField(blank=True, max_length=40, verbose_name="отчество")),
                ("account", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="manager", to=settings.AUTH_USER_MODEL, verbose_name="аккаунт")),
            ],
            options={
                "verbose_name": "Менеджер учебной части",
                "verbose_name_plural": "Менеджеры учебной части",
                "ordering": ["last_name", "first_name", "patronymic"],
            },
        ),
    ]

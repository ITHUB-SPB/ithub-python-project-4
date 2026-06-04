import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0002_update_user_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="Manager",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=20, verbose_name="имя")),
                ("last_name", models.CharField(max_length=40, verbose_name="фамилия")),
                ("middle_name", models.CharField(blank=True, max_length=40, verbose_name="отчество")),
                (
                    "account",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="manager",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="аккаунт",
                    ),
                ),
            ],
            options={
                "verbose_name": "менеджер",
                "verbose_name_plural": "менеджеры",
                "ordering": ["-last_name", "-first_name", "-middle_name"],
            },
        ),
        migrations.CreateModel(
            name="Teacher",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=20, verbose_name="имя")),
                ("last_name", models.CharField(max_length=40, verbose_name="фамилия")),
                ("middle_name", models.CharField(blank=True, max_length=40, verbose_name="отчество")),
                (
                    "account",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="teacher",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="аккаунт",
                    ),
                ),
            ],
            options={
                "verbose_name": "преподаватель",
                "verbose_name_plural": "преподаватели",
                "ordering": ["-last_name", "-first_name", "-middle_name"],
            },
        ),
    ]

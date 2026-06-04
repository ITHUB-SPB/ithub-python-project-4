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
            name="Group",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=15, verbose_name="название")),
                (
                    "course",
                    models.CharField(
                        choices=[("1", "1 курс"), ("2", "2 курс"), ("3", "3 курс"), ("4", "4 курс")],
                        max_length=1,
                        verbose_name="курс",
                    ),
                ),
            ],
            options={
                "verbose_name": "учебная группа",
                "verbose_name_plural": "учебные группы",
                "ordering": ["course", "title"],
            },
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=20, verbose_name="имя")),
                ("last_name", models.CharField(max_length=40, verbose_name="фамилия")),
                ("middle_name", models.CharField(blank=True, max_length=40, verbose_name="отчество")),
                (
                    "account",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="student",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="аккаунт",
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="students",
                        to="students.group",
                        verbose_name="группа",
                    ),
                ),
            ],
            options={
                "verbose_name": "студент",
                "verbose_name_plural": "студенты",
                "ordering": ["last_name", "first_name"],
            },
        ),
        migrations.AddIndex(
            model_name="group",
            index=models.Index(fields=["course"], name="students_gr_course_1f7b78_idx"),
        ),
        migrations.AddIndex(
            model_name="student",
            index=models.Index(fields=["last_name", "first_name"], name="students_st_last_na_6c440c_idx"),
        ),
    ]

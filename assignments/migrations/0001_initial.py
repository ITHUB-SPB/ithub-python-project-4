import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("courses", "0001_initial"),
        ("students", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Assignment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("weight", models.PositiveIntegerField(verbose_name="максимальный балл")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="обновлено")),
                (
                    "topic",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="assignment",
                        to="courses.topic",
                        verbose_name="тема",
                    ),
                ),
            ],
            options={
                "verbose_name": "контрольная точка",
                "verbose_name_plural": "контрольные точки",
                "ordering": ["topic__discipline", "topic__ordering_number"],
            },
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("answer", models.TextField(verbose_name="ответ")),
                ("score", models.PositiveIntegerField(blank=True, null=True, verbose_name="оценка")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="обновлено")),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="assignments.assignment",
                        verbose_name="контрольная точка",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="students.student",
                        verbose_name="студент",
                    ),
                ),
            ],
            options={
                "verbose_name": "ответ",
                "verbose_name_plural": "ответы",
                "ordering": ["assignment__topic__discipline", "assignment__topic__ordering_number"],
            },
        ),
        migrations.AddConstraint(
            model_name="submission",
            constraint=models.UniqueConstraint(fields=("student", "assignment"), name="unique_submission"),
        ),
    ]

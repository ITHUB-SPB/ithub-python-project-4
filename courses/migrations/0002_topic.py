import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Topic",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ordering_number", models.PositiveIntegerField(verbose_name="порядковый номер")),
                ("title", models.CharField(max_length=50, verbose_name="название")),
                ("content", models.TextField(verbose_name="содержимое")),
                ("duration", models.PositiveIntegerField(verbose_name="количество часов")),
                (
                    "discipline",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="topics",
                        to="courses.discipline",
                        verbose_name="дисциплина",
                    ),
                ),
            ],
            options={
                "verbose_name": "Учебная тема",
                "verbose_name_plural": "Учебные темы",
                "ordering": ["discipline_id", "ordering_number"],
            },
        ),
        migrations.AddConstraint(
            model_name="topic",
            constraint=models.UniqueConstraint(
                fields=("ordering_number", "discipline"),
                name="unique_topic_ordering_number_discipline",
            ),
        ),
        migrations.AddIndex(
            model_name="topic",
            index=models.Index(fields=["discipline", "ordering_number"], name="courses_top_discipl_991b5d_idx"),
        ),
    ]

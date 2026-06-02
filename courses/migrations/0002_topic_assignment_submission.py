from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0001_initial"),
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Topic",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ordering_number", models.PositiveIntegerField(verbose_name="Номер")),
                ("title", models.CharField(max_length=50, verbose_name="Название")),
                ("content", models.TextField(verbose_name="Содержимое")),
                ("duration", models.PositiveIntegerField(verbose_name="Часы")),
                ("discipline", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="topics", to="courses.discipline", verbose_name="Дисциплина")),
            ],
            options={
                "verbose_name": "Топик",
                "verbose_name_plural": "Топики",
                "ordering": ["discipline_id", "ordering_number"],
            },
        ),
        migrations.CreateModel(
            name="Assignment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("weight", models.PositiveIntegerField(verbose_name="Максимальный балл")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлено")),
                ("topic", models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="assignment", to="courses.topic", verbose_name="Топик")),
            ],
            options={
                "verbose_name": "Контрольная точка",
                "verbose_name_plural": "Контрольные точки",
                "ordering": ["topic__discipline_id", "topic__ordering_number"],
            },
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("answer", models.TextField(verbose_name="Ответ")),
                ("score", models.PositiveIntegerField(blank=True, null=True, verbose_name="Оценка")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлено")),
                ("assignment", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="submissions", to="courses.assignment", verbose_name="Контрольная точка")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="submissions", to="students.student", verbose_name="Студент")),
            ],
            options={
                "verbose_name": "Ответ",
                "verbose_name_plural": "Ответы",
                "ordering": ["assignment__topic__discipline_id", "assignment__topic__ordering_number"],
            },
        ),
        migrations.AddConstraint(
            model_name="topic",
            constraint=models.UniqueConstraint(fields=("ordering_number", "discipline"), name="unique_topic_number_in_discipline"),
        ),
    ]

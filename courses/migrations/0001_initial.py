import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("staff", "0001_initial"),
        ("students", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Discipline",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=15, unique=True, verbose_name="код")),
                ("title", models.CharField(max_length=50, verbose_name="название")),
                (
                    "duration",
                    models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name="длительность"),
                ),
                ("curriculum", models.FileField(blank=True, null=True, upload_to="curriculums/", verbose_name="учебный план")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="обновлено")),
            ],
            options={
                "verbose_name": "дисциплина",
                "verbose_name_plural": "дисциплины",
                "ordering": ["-updated_at", "-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=15, verbose_name="код курса")),
                ("about", models.CharField(blank=True, max_length=200, verbose_name="описание")),
                ("course_start", models.DateField(blank=True, null=True, verbose_name="дата начала")),
                ("course_end", models.DateField(blank=True, null=True, verbose_name="дата окончания")),
                (
                    "discipline",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="courses",
                        to="courses.discipline",
                        verbose_name="дисциплина",
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="courses",
                        to="students.group",
                        verbose_name="группа",
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="courses",
                        to="staff.teacher",
                        verbose_name="преподаватель",
                    ),
                ),
            ],
            options={
                "verbose_name": "курс",
                "verbose_name_plural": "курсы",
                "ordering": ["discipline__code", "code"],
            },
        ),
        migrations.CreateModel(
            name="Topic",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ordering_number", models.PositiveIntegerField(verbose_name="номер")),
                ("title", models.CharField(max_length=50, verbose_name="название")),
                ("content", models.TextField(verbose_name="содержимое")),
                ("duration", models.PositiveIntegerField(verbose_name="часы")),
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
                "verbose_name": "тема",
                "verbose_name_plural": "темы",
                "ordering": ["discipline", "ordering_number"],
            },
        ),
        migrations.AddIndex(
            model_name="discipline",
            index=models.Index(fields=["code"], name="courses_dis_code_69073c_idx"),
        ),
        migrations.AddIndex(
            model_name="discipline",
            index=models.Index(fields=["title"], name="courses_dis_title_c985f3_idx"),
        ),
        migrations.AddIndex(
            model_name="discipline",
            index=models.Index(fields=["duration"], name="courses_dis_duration_6c4f92_idx"),
        ),
        migrations.AddIndex(
            model_name="course",
            index=models.Index(fields=["code"], name="courses_cou_code_7923bf_idx"),
        ),
        migrations.AddIndex(
            model_name="course",
            index=models.Index(fields=["course_start"], name="courses_cou_course__4287bf_idx"),
        ),
        migrations.AddIndex(
            model_name="course",
            index=models.Index(fields=["course_end"], name="courses_cou_course__f30f44_idx"),
        ),
        migrations.AddIndex(
            model_name="course",
            index=models.Index(fields=["group"], name="courses_cou_group_i_73b4dd_idx"),
        ),
        migrations.AddIndex(
            model_name="course",
            index=models.Index(fields=["teacher"], name="courses_cou_teacher_6324a8_idx"),
        ),
        migrations.AddConstraint(
            model_name="topic",
            constraint=models.UniqueConstraint(fields=("ordering_number", "discipline"), name="unique_topic_number_in_discipline"),
        ),
    ]

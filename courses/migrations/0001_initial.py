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
                ("title", models.CharField(max_length=50, verbose_name="название")),
                ("duration", models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name="длительность")),
                ("curriculum", models.FileField(blank=True, null=True, upload_to="curriculums/", verbose_name="учебный план")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="обновлено")),
            ],
            options={
                "verbose_name": "Дисциплина",
                "verbose_name_plural": "Дисциплины",
                "ordering": ["-updated_at", "-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=15, verbose_name="код")),
                ("about", models.CharField(blank=True, max_length=200, verbose_name="описание")),
                ("course_start", models.DateField(blank=True, null=True, verbose_name="начало курса")),
                ("course_end", models.DateField(blank=True, null=True, verbose_name="конец курса")),
                ("discipline", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="courses", to="courses.discipline", verbose_name="дисциплина")),
                ("group", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="courses", to="students.group", verbose_name="группа")),
                ("teacher", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="courses", to="staff.teacher", verbose_name="преподаватель")),
            ],
            options={
                "verbose_name": "Курс",
                "verbose_name_plural": "Курсы",
                "ordering": ["discipline_id", "code"],
            },
        ),
        migrations.AddIndex(
            model_name="discipline",
            index=models.Index(fields=["title"], name="courses_dis_title_661cee_idx"),
        ),
        migrations.AddIndex(
            model_name="discipline",
            index=models.Index(fields=["updated_at", "created_at"], name="courses_dis_updated_b0f0fa_idx"),
        ),
        migrations.AddIndex(
            model_name="course",
            index=models.Index(fields=["code"], name="courses_cou_code_0b80b8_idx"),
        ),
        migrations.AddIndex(
            model_name="course",
            index=models.Index(fields=["discipline"], name="courses_cou_discipl_f22d85_idx"),
        ),
        migrations.AddIndex(
            model_name="course",
            index=models.Index(fields=["group"], name="courses_cou_group_i_4404a5_idx"),
        ),
        migrations.AddIndex(
            model_name="course",
            index=models.Index(fields=["teacher"], name="courses_cou_teacher_d6e2dd_idx"),
        ),
    ]

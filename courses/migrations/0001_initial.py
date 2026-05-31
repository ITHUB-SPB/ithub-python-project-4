from django.db import migrations, models
import django.db.models.deletion


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
                ("title", models.CharField(max_length=50, verbose_name="Название")),
                ("duration", models.PositiveIntegerField(verbose_name="Длительность")),
                ("curriculum", models.FileField(blank=True, null=True, upload_to="curriculums/", verbose_name="Учебный план")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлено")),
            ],
            options={"verbose_name": "Дисциплина", "verbose_name_plural": "Дисциплины", "ordering": ["-updated_at", "-created_at"]},
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=15, verbose_name="Код")),
                ("about", models.CharField(blank=True, max_length=200, null=True, verbose_name="Описание")),
                ("course_start", models.DateField(blank=True, null=True, verbose_name="Начало")),
                ("course_end", models.DateField(blank=True, null=True, verbose_name="Конец")),
                ("discipline", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="courses.discipline", verbose_name="Дисциплина")),
                ("group", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="students.group", verbose_name="Группа")),
                ("teacher", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="staff.teacher", verbose_name="Преподаватель")),
            ],
            options={"verbose_name": "Курс", "verbose_name_plural": "Курсы", "ordering": ["discipline_id"]},
        ),
        migrations.AddIndex(model_name="discipline", index=models.Index(fields=["updated_at", "created_at"], name="courses_dis_updated_130654_idx")),
        migrations.AddIndex(model_name="course", index=models.Index(fields=["code"], name="courses_cou_code_a34320_idx")),
        migrations.AddIndex(model_name="course", index=models.Index(fields=["discipline"], name="courses_cou_discipl_4ce13b_idx")),
        migrations.AddIndex(model_name="course", index=models.Index(fields=["group"], name="courses_cou_group_i_86ddd6_idx")),
    ]

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Group",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=15, verbose_name="Название")),
                ("course", models.CharField(choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4")], max_length=1, verbose_name="Курс")),
            ],
            options={"verbose_name": "Группа", "verbose_name_plural": "Группы", "ordering": ["course"]},
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=20, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=40, verbose_name="Фамилия")),
                ("middle_name", models.CharField(blank=True, max_length=40, null=True, verbose_name="Отчество")),
                ("account", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="accounts.user", verbose_name="Аккаунт")),
                ("group", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="students.group", verbose_name="Группа")),
            ],
            options={"verbose_name": "Студент", "verbose_name_plural": "Студенты", "ordering": ["last_name", "first_name"]},
        ),
        migrations.AddIndex(model_name="group", index=models.Index(fields=["course"], name="students_gr_course_0ec7f2_idx")),
        migrations.AddIndex(model_name="student", index=models.Index(fields=["last_name", "first_name"], name="students_st_last_na_412bc6_idx")),
    ]

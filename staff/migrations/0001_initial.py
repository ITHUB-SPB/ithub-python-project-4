from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Manager",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=20, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=40, verbose_name="Фамилия")),
                ("middle_name", models.CharField(blank=True, max_length=40, null=True, verbose_name="Отчество")),
                ("account", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="accounts.user", verbose_name="Аккаунт")),
            ],
            options={"verbose_name": "Менеджер", "verbose_name_plural": "Менеджеры", "ordering": ["-last_name", "-first_name", "-middle_name"]},
        ),
        migrations.CreateModel(
            name="Teacher",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=20, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=40, verbose_name="Фамилия")),
                ("middle_name", models.CharField(blank=True, max_length=40, null=True, verbose_name="Отчество")),
                ("account", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="accounts.user", verbose_name="Аккаунт")),
            ],
            options={"verbose_name": "Преподаватель", "verbose_name_plural": "Преподаватели", "ordering": ["-last_name", "-first_name", "-middle_name"]},
        ),
    ]

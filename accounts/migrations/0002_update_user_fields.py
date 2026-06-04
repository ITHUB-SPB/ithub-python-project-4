from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "аккаунт", "verbose_name_plural": "аккаунты"},
        ),
        migrations.AlterField(
            model_name="user",
            name="is_staff",
            field=models.BooleanField(default=False, verbose_name="сотрудник"),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_superuser",
            field=models.BooleanField(default=False, verbose_name="менеджер"),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=150, unique=True, verbose_name="логин"),
        ),
        migrations.AddField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="активен"),
        ),
    ]

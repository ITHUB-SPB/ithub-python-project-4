from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.db import connection
from django.db.models import Q
from django.db.models.signals import post_migrate


def setup_groups(sender, **kwargs):
    manager_group, _ = Group.objects.get_or_create(name="managers")
    teacher_group, _ = Group.objects.get_or_create(name="teachers")

    manager_permissions = Permission.objects.filter(
        Q(content_type__app_label__in=["accounts", "students", "staff", "courses"], codename__startswith="add")
        | Q(content_type__app_label__in=["accounts", "students", "staff", "courses"], codename__startswith="change")
        | Q(content_type__app_label__in=["accounts", "students", "staff", "courses"], codename__startswith="delete")
        | Q(content_type__app_label__in=["accounts", "students", "staff", "courses"], codename__startswith="view")
        | Q(
            content_type__app_label="assignments",
            codename__in=[
                "add_assignment",
                "change_assignment",
                "delete_assignment",
                "view_assignment",
                "view_submission",
            ],
        )
    )
    teacher_permissions = Permission.objects.filter(
        content_type__app_label__in=["courses", "assignments"],
        codename__in=[
            "view_course",
            "view_topic",
            "view_assignment",
            "view_submission",
            "change_submission",
        ],
    )

    manager_group.permissions.set(manager_permissions)
    teacher_group.permissions.set(teacher_permissions)

    tables = set(connection.introspection.table_names())
    if "staff_teacher" not in tables or "staff_manager" not in tables:
        return

    User = apps.get_model("accounts", "User")
    Teacher = apps.get_model("staff", "Teacher")
    Manager = apps.get_model("staff", "Manager")

    for user in User.objects.filter(id__in=Teacher.objects.values_list("account_id", flat=True)):
        user.groups.add(teacher_group)
        if not user.is_staff:
            user.is_staff = True
            user.save(update_fields=["is_staff"])

    for user in User.objects.filter(id__in=Manager.objects.values_list("account_id", flat=True)):
        user.groups.add(manager_group)
        if not user.is_staff:
            user.is_staff = True
            user.save(update_fields=["is_staff"])


post_migrate.connect(setup_groups)

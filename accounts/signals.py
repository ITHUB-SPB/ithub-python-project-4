from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_roles(sender, **kwargs):
    teacher_group, _ = Group.objects.get_or_create(name="teachers")
    manager_group, _ = Group.objects.get_or_create(name="managers")

    teacher_permissions = Permission.objects.filter(
        codename__in=[
            "view_group",
            "view_discipline",
            "view_course",
            "view_topic",
            "view_assignment",
            "view_submission",
            "change_submission",
        ]
    )
    teacher_group.permissions.set(teacher_permissions)

    manager_permissions = Permission.objects.filter(
        codename__in=[
            "add_user",
            "change_user",
            "delete_user",
            "view_user",
            "add_group",
            "change_group",
            "delete_group",
            "view_group",
            "add_student",
            "change_student",
            "delete_student",
            "view_student",
            "add_teacher",
            "change_teacher",
            "delete_teacher",
            "view_teacher",
            "add_discipline",
            "change_discipline",
            "delete_discipline",
            "view_discipline",
            "add_course",
            "change_course",
            "delete_course",
            "view_course",
            "add_topic",
            "change_topic",
            "delete_topic",
            "view_topic",
            "add_assignment",
            "change_assignment",
            "delete_assignment",
            "view_assignment",
            "add_submission",
            "change_submission",
            "delete_submission",
            "view_submission",
        ]
    )
    manager_group.permissions.set(manager_permissions)

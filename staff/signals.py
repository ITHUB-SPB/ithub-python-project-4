from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from staff.models import Manager, Teacher


def permission_map():
    return {
        "managers": [
            "view_user",
            "add_user",
            "change_user",
            "delete_user",
            "view_group",
            "add_group",
            "change_group",
            "delete_group",
            "view_student",
            "add_student",
            "change_student",
            "delete_student",
            "view_teacher",
            "add_teacher",
            "change_teacher",
            "delete_teacher",
            "view_manager",
            "add_manager",
            "change_manager",
            "delete_manager",
            "view_discipline",
            "add_discipline",
            "change_discipline",
            "delete_discipline",
            "view_course",
            "add_course",
            "change_course",
            "delete_course",
            "view_topic",
            "add_topic",
            "change_topic",
            "delete_topic",
            "view_controlpoint",
            "add_controlpoint",
            "change_controlpoint",
            "delete_controlpoint",
            "view_submission",
            "change_submission",
        ],
        "teachers": [
            "view_course",
            "view_topic",
            "view_controlpoint",
            "view_submission",
            "change_submission",
        ],
    }


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    for group_name, permission_codes in permission_map().items():
        group, _ = Group.objects.get_or_create(name=group_name)
        permissions = Permission.objects.filter(codename__in=permission_codes)
        group.permissions.set(permissions)


def attach_account_to_group(account, group_name):
    group, _ = Group.objects.get_or_create(name=group_name)
    if not account.is_staff:
        account.is_staff = True
        account.save(update_fields=["is_staff"])
    group.user_set.add(account)


@receiver(post_save, sender=Teacher)
def attach_teacher_group(sender, instance, **kwargs):
    attach_account_to_group(instance.account, "teachers")


@receiver(post_save, sender=Manager)
def attach_manager_group(sender, instance, **kwargs):
    attach_account_to_group(instance.account, "managers")

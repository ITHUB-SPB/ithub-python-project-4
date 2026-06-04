from django.contrib.auth.models import Group
from django.db.models.signals import post_save

from staff.models import Manager, Teacher


def update_account_group(account, group_name):
    group, _ = Group.objects.get_or_create(name=group_name)
    account.groups.add(group)
    if not account.is_staff:
        account.is_staff = True
        account.save(update_fields=["is_staff"])


def teacher_saved(sender, instance, **kwargs):
    update_account_group(instance.account, "teachers")


def manager_saved(sender, instance, **kwargs):
    update_account_group(instance.account, "managers")


post_save.connect(teacher_saved, sender=Teacher)
post_save.connect(manager_saved, sender=Manager)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import User


@receiver(post_save, sender=User)
def assign_staff_permissions(sender, instance, created, **kwargs):
    if created and instance.is_staff and not instance.is_superuser:
        permissions = Permission.objects.filter(
            content_type__app_label__in=["courses", "assignments"],
            codename__in=[
                "view_course",
                "view_discipline",
                "view_topic",
                "view_assignment",
                "view_answer",
                "change_answer",
            ]
        )
        instance.user_permissions.add(*permissions)
from django.contrib import admin
from unfold.admin import ModelAdmin
from staff import models


@admin.register(models.Teacher)
class TeacherAdmin(ModelAdmin):
    list_display = ["last_name_with_initials", "account"]
    search_fields = ["last_name"]

    def last_name_with_initials(self, obj):
        initials = f"{obj.first_name[:1]}."
        if obj.patronymic:
            initials += f"{obj.patronymic[:1]}."
        return f"{obj.last_name} {initials}"

    last_name_with_initials.short_description = "преподаватель"


@admin.register(models.Manager)
class ManagerAdmin(ModelAdmin):
    list_display = ["last_name", "first_name", "account"]
    search_fields = ["last_name", "first_name"]

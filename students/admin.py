from django.contrib import admin
from unfold.admin import ModelAdmin
from students import models


@admin.register(models.Group)
class GroupAdmin(ModelAdmin):
    list_display = ["title", "course"]
    list_filter = ["course"]
    search_fields = ["title"]


@admin.register(models.Student)
class StudentAdmin(ModelAdmin):
    list_display = ["last_name_with_initials", "group", "account"]
    list_filter = ["group"]
    search_fields = ["last_name"]

    def last_name_with_initials(self, obj):
        initials = f"{obj.first_name[:1]}."
        if obj.patronymic:
            initials += f"{obj.patronymic[:1]}."
        return f"{obj.last_name} {initials}"

    last_name_with_initials.short_description = "студент"

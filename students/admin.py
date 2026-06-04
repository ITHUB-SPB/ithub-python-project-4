from django.contrib import admin
from unfold.admin import ModelAdmin

from students.models import Group, Student


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ["title", "course"]
    list_filter = ["course"]
    search_fields = ["title"]


@admin.register(Student)
class StudentAdmin(ModelAdmin):
    list_display = ["short_name", "group", "account"]
    list_filter = ["group"]
    search_fields = ["last_name"]

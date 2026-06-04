from django.contrib import admin
from unfold.admin import ModelAdmin

from staff.models import Manager, Teacher


@admin.register(Teacher)
class TeacherAdmin(ModelAdmin):
    list_display = ["short_name", "account"]
    search_fields = ["last_name"]


@admin.register(Manager)
class ManagerAdmin(ModelAdmin):
    list_display = ["last_name", "first_name", "account"]
    search_fields = ["last_name"]

from django.contrib import admin
from unfold.admin import ModelAdmin
from staff import models


@admin.register(models.Teacher)
class TeacherAdmin(ModelAdmin):
    list_display = ["last_name", "first_name"]
    search_fields = ["last_name", "first_name"]


@admin.register(models.Manager)
class ManagerAdmin(ModelAdmin):
    list_display = ["last_name", "first_name"]
    search_fields = ["last_name", "first_name"]

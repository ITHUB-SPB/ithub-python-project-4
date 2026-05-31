from django.contrib import admin
from unfold.admin import ModelAdmin
from students import models


@admin.register(models.Group)
class GroupAdmin(ModelAdmin):
    list_display = ["title", "course"]
    search_fields = ["title", "course"]


@admin.register(models.Student)
class StudentAdmin(ModelAdmin):
    list_display = ["last_name", "first_name", "group"]
    list_filter = ["group"]
    search_fields = ["last_name", "first_name"]

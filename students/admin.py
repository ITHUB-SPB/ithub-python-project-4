from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Group, Student


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ["title", "course"]


@admin.register(Student)
class StudentAdmin(ModelAdmin):
    list_display = ["surname", "name", "lastname", "group", "account"]
    search_fields = ["surname", "name"]
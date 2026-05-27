from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Teacher, Manager


@admin.register(Teacher)
class TeacherAdmin(ModelAdmin):
    list_display = ["surname", "name", "lastname", "account"]
    search_fields = ["surname", "name"]


@admin.register(Manager)
class ManagerAdmin(ModelAdmin):
    list_display = ["surname", "name", "lastname", "account"]
    search_fields = ["surname", "name"]

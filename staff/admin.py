from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Teacher, Manager

@admin.register(Teacher)
class TeacherAdmin(ModelAdmin):
    list_display = ['full_name', 'account']
    search_fields = ['last_name', 'first_name', 'account__username']
    autocomplete_fields = ['account']


@admin.register(Manager)
class ManagerAdmin(ModelAdmin):
    list_display = ['full_name', 'account']
    search_fields = ['last_name', 'first_name', 'account__username']
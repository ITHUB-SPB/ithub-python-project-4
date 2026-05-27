from django.contrib import admin

from staff.models import Teacher, Manager


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'middle_name', 'account']
    search_fields = ['last_name', 'first_name']


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'middle_name', 'account']
    search_fields = ['last_name', 'first_name']
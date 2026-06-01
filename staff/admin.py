from django.contrib import admin
from staff.models import Manager, Teacher
from unfold.admin import ModelAdmin

# Register your models here.
@admin.register(Teacher)
class TeacherAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'middle_name', 'account')
    search_fields = ('last_name', 'account__username', 'account__email')

@admin.register(Manager)
class ManagerAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'middle_name', 'account')
    search_fields = ('last_name', 'account__username', 'account__email')
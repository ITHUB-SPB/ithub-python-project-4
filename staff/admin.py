from django.contrib import admin
from staff.models import Manager, Teacher

# Register your models here.
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'middle_name', 'account')
    search_fields = ('last_name', 'account__username', 'account__email')

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'middle_name', 'account')
    search_fields = ('last_name', 'account__username', 'account__email')
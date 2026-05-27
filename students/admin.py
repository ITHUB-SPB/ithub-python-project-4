from django.contrib import admin

from students.models import Group, Student


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']
    list_filter = ['course']
    search_fields = ['title']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'middle_name', 'group', 'account']
    list_filter = ['group', 'group__course']
    search_fields = ['last_name', 'first_name']
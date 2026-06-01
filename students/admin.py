from django.contrib import admin
from unfold.admin import ModelAdmin
from students.models import Group, Student

class GroupAdmin(ModelAdmin):
    list_display = ['title', 'year']
    list_filter = ['year']
    search_fields = ['title']

admin.site.register(Group, GroupAdmin)

# Register your models here.
class StudentAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'middle_name', 'account', 'group')
    search_fields = ('last_name', 'account__username', 'account__email')

admin.site.register(Student, StudentAdmin)
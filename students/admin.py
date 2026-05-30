from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Student, Group

@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ['name', 'course', 'student_count']
    list_filter = ['course']
    search_fields = ['name']
    
    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'кол-во студентов'


@admin.register(Student)
class StudentAdmin(ModelAdmin):
    list_display = ['initials', 'group', 'account']
    list_filter = ['group__course']
    search_fields = ['last_name', 'first_name', 'account__username']
    autocomplete_fields = ['group', 'account']
    
    def initials(self, obj):
        return obj.initials
    initials.short_description = 'ФИО'
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Student, Group

class StudentInline(admin.TabularInline):
    model = Student
    extra = 0
    fields = ('last_name', 'first_name', 'patronymic', 'account')
    readonly_fields = ('account',)
    show_change_link = True
    can_delete = False

@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ['name', 'course', 'student_count']
    list_filter = ['course']
    search_fields = ['name']
    inlines = [StudentInline]

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
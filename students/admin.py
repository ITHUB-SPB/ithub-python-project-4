from django.contrib import admin
from students.models import Group, Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'fio_short',
        'group',
        'account',
    ]

    list_filter = [
        'group',
    ]

    search_fields = [
        'last_name',
    ]

    def fio_short(self, obj):
        result = obj.last_name
        result += f' {obj.first_name[0]}.'

        if obj.middle_name:
            result += f' {obj.middle_name[0]}.'

        return result

    fio_short.short_description = 'ФИО'
    
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'course',
    ]

    list_filter = [
        'course',
    ]

    search_fields = [
        'title',
    ]
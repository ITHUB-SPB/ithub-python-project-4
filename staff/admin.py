from django.contrib import admin
from .models import Teacher, Manager

admin.site.register(Manager)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = [
        'fio_short',
        'account',
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
from django.contrib import admin
from courses import models


class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration']
    list_filter = ['duration']
    search_fields = ['title']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'discipline__title', 'discipline__duration', 'group']
    list_filter = ['discipline', 'discipline__duration', 'group', 'group__course']
    search_fields = ['code', 'discipline__title']


admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Discipline, DisciplineAdmin)
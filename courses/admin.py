from django.contrib import admin
from courses import models


class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'duration', 'curriculum', 'updated_at']
    list_filter = ['title', 'duration']
    search_fields = ['code', 'title']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['discipline__code', 'discipline__title', 'discipline__duration', 'course_start',
                    'course_end', 'teacher']
    list_filter = ['teacher', 'discipline__duration', 'course_start', 'course_end']
    search_fields = ['discipline__code', 'discipline__title']


admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Discipline, DisciplineAdmin)
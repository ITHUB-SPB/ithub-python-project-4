from django.contrib import admin

from courses.models import Discipline, Course


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'created_at', 'updated_at']
    search_fields = ['title']
    list_filter = ['duration']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'discipline', 'group', 'teacher', 'course_start', 'course_end']
    list_filter = ['discipline', 'group', 'teacher']
    search_fields = ['code', 'discipline__title']
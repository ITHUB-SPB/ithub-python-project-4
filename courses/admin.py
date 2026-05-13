from django.contrib import admin
from courses import models


class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'duration', 'curriculum', 'updated_at']
    list_filter = ['title', 'duration', 'course_start']
    search_fields = ['code', 'title']



admin.site.register(models.Course, CourseAdmin)
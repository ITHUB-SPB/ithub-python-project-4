from django.contrib import admin
from courses import models


class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'duration', 'curriculum', 'updated_at']
    list_filter = ['title', 'duration']
    search_fields = ['code', 'title']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['discipline__code', 'discipline__title', 'discipline__duration', 'course_start',
                    'course_end', 'teacher', 'group']
    list_filter = ['teacher', 'discipline__duration', 'course_start', 'course_end', 'group__title',
                   'group__course']
    search_fields = ['discipline__code', 'discipline__title']


class TopicAdmin(admin.ModelAdmin):
    list_display = ['discipline__title', 'title']
    list_filter = ['discipline']
    search_fields = ['discipline__title', 'title']


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['topic__discipline__title', 'topic__title', 'weight']
    list_filter = ['topic__discipline']
    search_fields = ['topic__discipline__title', 'topic__title']


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment__topic__discipline', 'assignment__topic__title']
    list_filter = ['student', 'assignment__topic__discipline']


admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Discipline, DisciplineAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Assignment, AssignmentAdmin)
admin.site.register(models.Submission, SubmissionAdmin)
from django.contrib import admin
from courses import models


class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration']
    list_filter = ['duration']
    search_fields = ['title']


class CoursesAdmin(admin.ModelAdmin):
    list_display = ['code', 'discipline', 'group']
    list_filter = ['discipline', 'group']
    search_fields = ['code', 'discipline__title']


class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'discipline']
    list_filter = ['discipline']


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['topic__discipline__title', 'topic__title', 'weight']
    list_filter = ['topic__discipline']


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment__topic__discipline', 'assignment__topic__title', 'score']
    list_filter = ['student', 'assignment__topic__discipline', 'score']


admin.site.register(models.Course, CoursesAdmin)
admin.site.register(models.Disclipline, DisciplineAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Assignment, AssignmentAdmin)
admin.site.register(models.Submission, SubmissionAdmin)



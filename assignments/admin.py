from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Assignment, Submission


@admin.register(Assignment)
class AssignmentAdmin(ModelAdmin):
    list_display = ['topic', 'weight', 'created_at']
    list_filter = ['topic__discipline']
    search_fields = ['topic__title']


@admin.register(Submission)
class SubmissionAdmin(ModelAdmin):
    list_display = ['student', 'assignment', 'score', 'created_at']
    list_filter = ['assignment__topic__discipline', 'score']
    search_fields = ['student__last_name', 'student__first_name']
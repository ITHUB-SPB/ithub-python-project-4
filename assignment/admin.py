from django.contrib import admin
from assignment import models

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['topic__title', 'weight', 'updated_at']


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment__topic__title', 'score']
    list_filter = ['assignment__topic__discipline']


admin.site.register(models.Assignment, AssignmentAdmin)
admin.site.register(models.Submission, SubmissionAdmin)
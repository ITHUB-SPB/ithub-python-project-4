from django.contrib import admin
from unfold.admin import ModelAdmin
from django.http import HttpResponse
import csv
from .models import Assignment, Submission

@admin.register(Assignment)
class AssignmentAdmin(ModelAdmin):
    list_display = ['topic', 'weight']
    search_fields = ['topic__title']
    autocomplete_fields = ['topic']


@admin.register(Submission)
class SubmissionAdmin(ModelAdmin):
    list_display = ['student', 'assignment', 'score', 'created_at']
    list_filter = ['assignment__topic__discipline']
    search_fields = ['student__last_name', 'assignment__topic__title']
    actions = ['export_to_csv']
    
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="submissions.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Студент', 'Контрольная точка', 'Оценка', 'Ответ', 'Дата'])
        
        for submission in queryset:
            writer.writerow([
                submission.student.full_name,
                str(submission.assignment),
                f"{submission.score}/{submission.assignment.weight}" if submission.score else "На проверке",
                submission.answer,
                submission.created_at.strftime('%Y-%m-%d %H:%M')
            ])
        
        return response
    export_to_csv.short_description = "Экспорт в CSV"
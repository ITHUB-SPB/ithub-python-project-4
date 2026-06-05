from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Assignment, Submission


@admin.register(Assignment)
class AssignmentAdmin(ModelAdmin):
    list_display = ['id', 'topic', 'weight', 'created_at']
    list_filter = ['weight', 'created_at']
    search_fields = ['topic__title']
    raw_id_fields = ['topic']


@admin.register(Submission)
class SubmissionAdmin(ModelAdmin):
    list_display = ['id', 'student', 'assignment', 'score', 'created_at']
    list_filter = ['score', 'created_at']
    search_fields = ['student__last_name', 'student__first_name', 'answer']
    raw_id_fields = ['student', 'assignment']
    
    actions = ['export_submissions']
    
    def export_submissions(self, request, queryset):
        """Экспорт ответов в CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="submissions.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Студент', 'Группа', 'Контрольная точка', 'Ответ', 'Оценка', 'Дата'])
        
        for sub in queryset:
            writer.writerow([
                sub.id,
                str(sub.student),
                sub.student.group.name if sub.student.group else '-',
                str(sub.assignment),
                sub.answer[:200],
                sub.score if sub.score is not None else 'На проверке',
                sub.created_at.strftime('%Y-%m-%d %H:%M')
            ])
        
        return response
    export_submissions.short_description = "Экспортировать выбранные ответы в CSV"
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Discipline, Course, Topic

@admin.register(Discipline)
class DisciplineAdmin(ModelAdmin):
    list_display = ['title', 'duration', 'created_at', 'updated_at']
    list_filter = ['duration']
    search_fields = ['title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = [
        'code', 'discipline', 'group', 'teacher', 
        'course_start', 'course_end'
    ]
    list_filter = ['group__course', 'discipline__duration']
    search_fields = ['code', 'discipline__title']
    autocomplete_fields = ['discipline', 'group', 'teacher']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'teacher_profile'):
            return qs.filter(teacher=request.user.teacher_profile)
        return qs

@admin.register(Topic)
class TopicAdmin(ModelAdmin):
    list_display = ['ordering_number', 'title', 'discipline', 'duration']
    list_filter = ['discipline']
    search_fields = ['title', 'discipline__title']
    autocomplete_fields = ['discipline']
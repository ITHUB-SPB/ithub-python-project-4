from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin

from courses.models import Assignment, Course, Discipline, Submission, Topic
from unfold.admin import ModelAdmin

# Register your models here.
@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ('code', 'about', 'discipline', 'teacher', 'group')
    list_filter = ('teacher', 'group')
    search_fields = ('code', 'discipline', 'teacher', 'group')
    def get_queryset(self, request):
        if request.user.groups.filter(name='teachers').exists():
            return super().get_queryset(request).filter(teacher=request.user.teacher) 
        else:
            return super().get_queryset(request)

@admin.register(Discipline)
class DisciplineAdmin(ModelAdmin):
    list_display = ('title', 'duration', 'curriculum', 'created_at', 'updated_at')
    search_fields = ('title',)

@admin.register(Topic)
class TopicAdmin(ModelAdmin):
    list_display = ('orderingnumber', 'title', 'discipline')
    search_fields = ('discipline',)

@admin.register(Assignment)
class AssignmentAdmin(ModelAdmin):
    list_display = ('topic__discipline__title', 'topic__title', 'weight', 'created_at', 'updated_at', 'content')
    search_fields = ('topic__title',)

@admin.register(Submission)
class SubmissionAdmin(ModelAdmin):
    list_display = ('assignment__topic__title', 'student', 'assignment', 'score', 'answer')
    search_fields = ('student__username',)

    readonly_fields = ('student', 'assignment', 'answer')
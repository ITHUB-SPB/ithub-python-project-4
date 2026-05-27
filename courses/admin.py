from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Discipline, Course, Topic
from staff.models import Teacher


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ["code", "discipline", "group", "teacher"]
    list_filter = ["group", "teacher"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            teacher = Teacher.objects.get(account=request.user)
            return qs.filter(teacher=teacher)
        except Teacher.DoesNotExist:
            return qs.none()


@admin.register(Discipline)
class DisciplineAdmin(ModelAdmin):
    list_display = ["title", "duration"]


@admin.register(Topic)
class TopicAdmin(ModelAdmin):
    list_display = ["title", "discipline", "order"]
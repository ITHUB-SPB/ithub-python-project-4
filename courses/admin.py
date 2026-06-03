from django.contrib import admin
from unfold.admin import ModelAdmin
from courses import models


def is_teacher(user):
    return user.is_authenticated and user.groups.filter(name="teachers").exists()


@admin.register(models.Discipline)
class DisciplineAdmin(ModelAdmin):
    list_display = ["title", "duration", "curriculum", "updated_at"]
    list_filter = ["title", "duration"]
    search_fields = ["title"]


@admin.register(models.Course)
class CourseAdmin(ModelAdmin):
    list_display = [
        "code",
        "discipline_title",
        "discipline_duration",
        "course_start",
        "course_end",
        "teacher",
        "group",
    ]
    list_filter = ["teacher", "group", "course_start", "course_end"]
    search_fields = ["code", "discipline__title"]

    def discipline_title(self, obj):
        if obj.discipline:
            return obj.discipline.title
        return "-"

    discipline_title.short_description = "дисциплина"

    def discipline_duration(self, obj):
        if obj.discipline:
            return obj.discipline.duration
        return "-"

    discipline_duration.short_description = "длительность"

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related("discipline", "teacher", "group")
        if is_teacher(request.user) and hasattr(request.user, "teacher"):
            return queryset.filter(teacher=request.user.teacher)
        return queryset


@admin.register(models.Topic)
class TopicAdmin(ModelAdmin):
    list_display = ["ordering_number", "title", "discipline", "duration"]
    list_filter = ["discipline"]
    search_fields = ["title", "discipline__title"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related("discipline")
        if is_teacher(request.user) and hasattr(request.user, "teacher"):
            return queryset.filter(discipline__courses__teacher=request.user.teacher).distinct()
        return queryset

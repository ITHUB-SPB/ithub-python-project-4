from django.contrib import admin
from unfold.admin import ModelAdmin

from assignments import models


def is_teacher(user):
    return user.is_authenticated and user.groups.filter(name="teachers").exists()


@admin.register(models.Assignment)
class AssignmentAdmin(ModelAdmin):
    list_display = ["topic", "discipline_title", "weight", "updated_at"]
    list_filter = ["topic", "weight"]
    search_fields = ["topic__title", "topic__discipline__title"]

    def discipline_title(self, obj):
        if obj.topic and obj.topic.discipline:
            return obj.topic.discipline.title
        return "-"

    discipline_title.short_description = "дисциплина"

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related("topic", "topic__discipline")
        if is_teacher(request.user) and hasattr(request.user, "teacher"):
            return queryset.filter(topic__discipline__courses__teacher=request.user.teacher).distinct()
        return queryset


@admin.register(models.Submission)
class SubmissionAdmin(ModelAdmin):
    list_display = ["student", "assignment", "score", "updated_at"]
    list_filter = ["assignment", "score"]
    search_fields = ["student__last_name", "student__first_name", "assignment__topic__title"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related(
            "student",
            "assignment",
            "assignment__topic",
            "assignment__topic__discipline",
        )
        if is_teacher(request.user) and hasattr(request.user, "teacher"):
            return queryset.filter(
                assignment__topic__discipline__courses__teacher=request.user.teacher
            ).distinct()
        return queryset

    def get_readonly_fields(self, request, obj=None):
        if is_teacher(request.user):
            return ["student", "assignment", "answer", "created_at", "updated_at"]
        return []

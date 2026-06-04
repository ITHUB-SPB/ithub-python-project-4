from django.contrib import admin
from unfold.admin import ModelAdmin

from assignments.models import Assignment, Submission


class TeacherLimitedAdmin(ModelAdmin):
    def is_manager(self, request):
        return request.user.is_superuser or request.user.groups.filter(name="managers").exists()

    def current_teacher(self, request):
        return getattr(request.user, "teacher", None)


@admin.register(Assignment)
class AssignmentAdmin(TeacherLimitedAdmin):
    list_display = [
        "discipline_code",
        "discipline_title",
        "topic_title",
        "weight",
        "teachers_for_assignment",
        "groups_for_assignment",
        "updated_at",
    ]
    search_fields = ["topic__title", "topic__discipline__code", "topic__discipline__title"]
    list_select_related = ["topic", "topic__discipline"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related("topic", "topic__discipline").prefetch_related(
            "topic__discipline__courses__teacher",
            "topic__discipline__courses__group",
        )
        if self.is_manager(request):
            return queryset
        teacher = self.current_teacher(request)
        if teacher:
            return queryset.filter(topic__discipline__courses__teacher=teacher).distinct()
        return queryset.none()

    def get_list_filter(self, request):
        filters = [
            "weight",
            "topic__discipline__courses__group",
            "topic__discipline__courses__group__course",
            "created_at",
            "updated_at",
        ]
        if self.is_manager(request):
            return ["topic__discipline__courses__teacher", *filters]
        return filters

    @admin.display(description="код дисциплины")
    def discipline_code(self, obj):
        return obj.topic.discipline.code if obj.topic and obj.topic.discipline else ""

    @admin.display(description="название дисциплины")
    def discipline_title(self, obj):
        return obj.topic.discipline.title if obj.topic and obj.topic.discipline else ""

    @admin.display(description="тема")
    def topic_title(self, obj):
        return obj.topic.title if obj.topic else ""

    @admin.display(description="преподаватели")
    def teachers_for_assignment(self, obj):
        if not obj.topic or not obj.topic.discipline:
            return ""
        teachers = obj.topic.discipline.courses.select_related("teacher").values_list(
            "teacher__last_name",
            "teacher__first_name",
            "teacher__middle_name",
        ).distinct()
        result = []
        for last_name, first_name, middle_name in teachers:
            if not last_name or not first_name:
                continue
            initials = first_name[:1]
            if middle_name:
                initials += f".{middle_name[:1]}"
            result.append(f"{last_name} {initials}.")
        return ", ".join(result)

    @admin.display(description="группы")
    def groups_for_assignment(self, obj):
        if not obj.topic or not obj.topic.discipline:
            return ""
        groups = obj.topic.discipline.courses.select_related("group").values_list("group__title", flat=True).distinct()
        return ", ".join(groups)


@admin.register(Submission)
class SubmissionAdmin(TeacherLimitedAdmin):
    list_display = [
        "student_name",
        "student_group",
        "discipline_code",
        "topic_title",
        "score_display",
        "created_at",
        "updated_at",
    ]
    search_fields = ["student__last_name", "assignment__topic__title", "assignment__topic__discipline__code"]
    list_select_related = ["student", "student__group", "assignment", "assignment__topic", "assignment__topic__discipline"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related(
            "student",
            "student__group",
            "assignment",
            "assignment__topic",
            "assignment__topic__discipline",
        )
        if self.is_manager(request):
            return queryset
        teacher = self.current_teacher(request)
        if teacher:
            return queryset.filter(assignment__topic__discipline__courses__teacher=teacher).distinct()
        return queryset.none()

    def get_list_filter(self, request):
        filters = [
            "score",
            "student__group",
            "student__group__course",
            "created_at",
            "updated_at",
        ]
        if self.is_manager(request):
            return ["assignment__topic__discipline__courses__teacher", *filters]
        return filters

    def get_readonly_fields(self, request, obj=None):
        if self.is_manager(request):
            return []
        return ["student", "assignment", "answer", "created_at", "updated_at"]

    @admin.display(description="студент")
    def student_name(self, obj):
        return obj.student.short_name()

    @admin.display(description="группа")
    def student_group(self, obj):
        return obj.student.group

    @admin.display(description="код дисциплины")
    def discipline_code(self, obj):
        return obj.assignment.topic.discipline.code if obj.assignment.topic and obj.assignment.topic.discipline else ""

    @admin.display(description="тема")
    def topic_title(self, obj):
        return obj.assignment.topic.title if obj.assignment.topic else ""

    @admin.display(description="баллы")
    def score_display(self, obj):
        if obj.score is None:
            return f"На проверке / {obj.assignment.weight}"
        return f"{obj.score} / {obj.assignment.weight}"

from csv import writer

from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone

from unfold.admin import ModelAdmin

from courses.models import ControlPoint, Course, Discipline, Submission, Topic


def is_manager(user):
    return user.is_superuser or user.groups.filter(name="managers").exists()


def is_teacher(user):
    return user.groups.filter(name="teachers").exists() and hasattr(user, "teacher")


class TeacherScopedAdmin(ModelAdmin):
    def has_add_permission(self, request):
        return super().has_add_permission(request) and not is_teacher(request.user)

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and not is_teacher(request.user)


@admin.register(Discipline)
class DisciplineAdmin(TeacherScopedAdmin):
    list_display = ("title", "duration", "curriculum", "updated_at", "topics_list")
    list_filter = ("duration",)
    search_fields = ("title",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related("topics")
        if is_teacher(request.user):
            return queryset.filter(courses__teacher=request.user.teacher).distinct()
        return queryset

    @admin.display(description="Темы")
    def topics_list(self, obj):
        return ", ".join(topic.title for topic in obj.topics.all()) or "-"


@admin.register(Course)
class CourseAdmin(TeacherScopedAdmin):
    list_display = ("code", "discipline", "discipline_duration", "course_start", "course_end", "teacher", "group")
    list_filter = ("teacher", "group", "course_start", "course_end", "discipline")
    search_fields = ("code", "discipline__title", "group__name")

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related("discipline", "teacher", "group")
        if is_teacher(request.user):
            return queryset.filter(teacher=request.user.teacher)
        return queryset

    @admin.display(description="Длительность")
    def discipline_duration(self, obj):
        return obj.discipline.duration if obj.discipline else "-"


@admin.register(Topic)
class TopicAdmin(TeacherScopedAdmin):
    list_display = ("title", "discipline", "study_hours", "order")
    list_filter = ("discipline", "study_hours")
    search_fields = ("title", "discipline__title")

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related("discipline")
        if is_teacher(request.user):
            return queryset.filter(discipline__courses__teacher=request.user.teacher).distinct()
        return queryset


@admin.register(ControlPoint)
class ControlPointAdmin(TeacherScopedAdmin):
    list_display = ("title", "topic", "discipline_title", "max_score")
    list_filter = ("max_score", "topic__discipline")
    search_fields = ("title", "topic__title", "topic__discipline__title")

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related("topic", "topic__discipline")
        if is_teacher(request.user):
            return queryset.filter(topic__discipline__courses__teacher=request.user.teacher).distinct()
        return queryset

    @admin.display(description="Дисциплина")
    def discipline_title(self, obj):
        return obj.topic.discipline


@admin.register(Submission)
class SubmissionAdmin(ModelAdmin):
    list_display = ("student", "course", "control_point", "score", "created_at", "reviewed_at")
    list_filter = ("course", "control_point", "score")
    search_fields = ("student__last_name", "student__first_name", "course__code", "control_point__title")
    actions = ("export_to_csv",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related(
            "student",
            "course",
            "control_point",
            "control_point__topic",
        )
        if is_teacher(request.user):
            return queryset.filter(course__teacher=request.user.teacher)
        return queryset

    def get_readonly_fields(self, request, obj=None):
        if is_teacher(request.user):
            return ("course", "control_point", "student", "message", "attachment", "created_at", "reviewed_at")
        return ()

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return is_manager(request.user) and super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if "score" in form.changed_data:
            obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)

    @admin.action(description="Экспортировать в CSV")
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="submissions.csv"'
        csv_writer = writer(response)
        csv_writer.writerow(["Студент", "Курс", "Контрольная точка", "Оценка", "Отправлено"])
        for submission in queryset.select_related("student", "course", "control_point"):
            csv_writer.writerow(
                [
                    submission.student.full_name,
                    str(submission.course),
                    submission.control_point.title,
                    submission.score or "",
                    submission.created_at.strftime("%Y-%m-%d %H:%M"),
                ]
            )
        return response

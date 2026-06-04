from django.contrib import admin
from unfold.admin import ModelAdmin

from courses.models import Course, Discipline, Topic
from staff.models import Teacher


class TeacherLimitedAdmin(ModelAdmin):
    def is_manager(self, request):
        return request.user.is_superuser or request.user.groups.filter(name="managers").exists()

    def current_teacher(self, request):
        return getattr(request.user, "teacher", None)


@admin.register(Discipline)
class DisciplineAdmin(TeacherLimitedAdmin):
    list_display = ["code", "title", "duration", "curriculum", "updated_at"]
    list_filter = ["title", "duration"]
    search_fields = ["code", "title"]


@admin.register(Course)
class CourseAdmin(TeacherLimitedAdmin):
    list_display = [
        "discipline_code",
        "discipline_title",
        "discipline_duration",
        "course_start",
        "course_end",
        "teacher",
        "group",
    ]
    search_fields = ["discipline__code", "discipline__title"]
    list_select_related = ["discipline", "teacher", "group"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related("discipline", "teacher", "group")
        if self.is_manager(request):
            return queryset
        teacher = self.current_teacher(request)
        if teacher:
            return queryset.filter(teacher=teacher)
        return queryset.none()

    def get_list_filter(self, request):
        filters = ["discipline__duration", "course_start", "course_end", "group", "group__course"]
        if self.is_manager(request):
            return ["teacher", *filters]
        return filters

    @admin.display(description="код дисциплины")
    def discipline_code(self, obj):
        return obj.discipline.code if obj.discipline else ""

    @admin.display(description="название дисциплины")
    def discipline_title(self, obj):
        return obj.discipline.title if obj.discipline else ""

    @admin.display(description="длительность")
    def discipline_duration(self, obj):
        return obj.discipline.duration if obj.discipline else ""


@admin.register(Topic)
class TopicAdmin(TeacherLimitedAdmin):
    list_display = [
        "discipline_code",
        "discipline_title",
        "discipline_duration",
        "course_start",
        "course_end",
        "teachers_for_topic",
        "groups_for_topic",
    ]
    search_fields = ["discipline__code", "discipline__title", "title"]
    list_select_related = ["discipline"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related("discipline").prefetch_related(
            "discipline__courses__group",
            "discipline__courses__teacher",
        ).distinct()
        if self.is_manager(request):
            return queryset
        teacher = self.current_teacher(request)
        if teacher:
            return queryset.filter(discipline__courses__teacher=teacher).distinct()
        return queryset.none()

    def get_list_filter(self, request):
        filters = [
            "duration",
            "discipline__courses__course_start",
            "discipline__courses__course_end",
            "discipline__courses__group",
            "discipline__courses__group__course",
        ]
        if self.is_manager(request):
            return ["discipline__courses__teacher", *filters]
        return filters

    @admin.display(description="код дисциплины")
    def discipline_code(self, obj):
        return obj.discipline.code if obj.discipline else ""

    @admin.display(description="название дисциплины")
    def discipline_title(self, obj):
        return obj.discipline.title if obj.discipline else ""

    @admin.display(description="длительность дисциплины")
    def discipline_duration(self, obj):
        return obj.discipline.duration if obj.discipline else ""

    @admin.display(description="дата начала")
    def course_start(self, obj):
        course = obj.discipline.courses.order_by("course_start").first() if obj.discipline else None
        return course.course_start if course else ""

    @admin.display(description="дата окончания")
    def course_end(self, obj):
        course = obj.discipline.courses.order_by("course_end").last() if obj.discipline else None
        return course.course_end if course else ""

    @admin.display(description="преподаватели")
    def teachers_for_topic(self, obj):
        return ", ".join(
            teacher.short_name() for teacher in Teacher.objects.filter(courses__discipline=obj.discipline).distinct()
        )

    @admin.display(description="группы")
    def groups_for_topic(self, obj):
        groups = obj.discipline.courses.select_related("group").values_list("group__title", flat=True).distinct()
        return ", ".join(groups)

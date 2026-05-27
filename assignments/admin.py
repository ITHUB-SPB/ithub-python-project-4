from django.contrib import admin
from .models import Assignment, Answer
from courses.models import Course
from staff.models import Teacher
from unfold.admin import ModelAdmin


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    fields = ["student", "value", "score"]
    readonly_fields = ["student", "value"]
    can_delete = False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            teacher = Teacher.objects.get(account=request.user)
            courses = Course.objects.filter(teacher=teacher)
            disciplines = courses.values_list("discipline", flat=True)
            return qs.filter(assignment__discipline__in=disciplines)
        except Teacher.DoesNotExist:
            return qs.none()


@admin.register(Assignment)
class AssignmentAdmin(ModelAdmin):
    list_display = ["title", "discipline", "order", "weight"]
    list_filter = ["discipline"]
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(ModelAdmin):
    list_display = ["student", "assignment", "score", "value_preview"]
    list_editable = ["score"]
    list_filter = ["assignment__discipline"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            teacher = Teacher.objects.get(account=request.user)
            courses = Course.objects.filter(teacher=teacher)
            disciplines = courses.values_list("discipline", flat=True)
            return qs.filter(assignment__discipline__in=disciplines)
        except Teacher.DoesNotExist:
            return qs.none()

    def value_preview(self, obj):
        return obj.value[:50] + "..." if len(obj.value) > 50 else obj.value
    value_preview.short_description = "ответ"
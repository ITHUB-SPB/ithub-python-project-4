from django.contrib import admin
from unfold.admin import ModelAdmin
from courses import models


@admin.register(models.Discipline)
class DisciplineAdmin(ModelAdmin):
    list_display = ["title", "duration", "updated_at"]
    search_fields = ["title"]


@admin.register(models.Course)
class CourseAdmin(ModelAdmin):
    list_display = ["code", "discipline", "group", "teacher"]
    list_filter = ["discipline", "group", "teacher"]
    search_fields = ["code"]

from django.contrib import admin

from unfold.admin import ModelAdmin

from staff.models import Manager, Teacher


@admin.register(Teacher)
class TeacherAdmin(ModelAdmin):
    list_display = ("short_name", "account")
    search_fields = ("last_name", "first_name", "account__username")

    @admin.display(description="Преподаватель")
    def short_name(self, obj):
        return obj.short_name


@admin.register(Manager)
class ManagerAdmin(ModelAdmin):
    list_display = ("short_name", "account")
    search_fields = ("last_name", "first_name", "account__username")

    @admin.display(description="Менеджер")
    def short_name(self, obj):
        return obj.short_name

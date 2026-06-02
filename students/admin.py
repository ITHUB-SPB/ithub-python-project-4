from django.contrib import admin

from unfold.admin import ModelAdmin

from students.models import Group, Student


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ("name", "course", "students_list")
    list_filter = ("course",)
    search_fields = ("name",)

    @admin.display(description="Студенты")
    def students_list(self, obj):
        return ", ".join(student.short_name for student in obj.students.all()) or "-"


@admin.register(Student)
class StudentAdmin(ModelAdmin):
    list_display = ("short_name", "group", "account")
    list_filter = ("group",)
    search_fields = ("last_name", "first_name", "account__username")

    @admin.display(description="Студент")
    def short_name(self, obj):
        return obj.short_name

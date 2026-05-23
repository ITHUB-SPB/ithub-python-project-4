from django.contrib import admin

from courses.models import Course, Discipline

# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'about', 'discipline', 'teacher', 'group')
    search_fields = ('code', 'discipline', 'teacher', 'group')

@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'curriculum', 'created_at', 'updated_at')
    search_fields = ('title',)
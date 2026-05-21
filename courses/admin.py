from django.contrib import admin
from courses import models


class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration']
    list_filter = ['duration']
    search_fields = ['title']


class CoursesAdmin(admin.ModelAdmin):
    list_display = ['code', 'discipline', 'group']
    list_filter = ['discipline', 'group']
    search_fields = ['code', 'discipline__title']


admin.site.register(models.Course, CoursesAdmin)
admin.site.register(models.Disclipline, DisciplineAdmin)



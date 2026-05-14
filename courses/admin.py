from django.contrib import admin
from courses import models


class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'duration']
    list_filter = ['duration']
    search_fields = ['code', 'title']





admin.site.register(models.Disclipline, DisciplineAdmin)



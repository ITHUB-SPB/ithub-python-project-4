from django.contrib import admin
from courses import models


class DiscliplineAdmin(admin.ModelAdmin):
	list_display = ['code', 'title', 'duration']
	list_filter = ['duration']
	search_fields = ['code', 'title']

admin.site.register(models.Discipline, DiscliplineAdmin)
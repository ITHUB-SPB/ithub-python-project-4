from django.contrib import admin
from courses import models


class DiscliplineAdmin(admin.ModelAdmin):
	list_display = ['title', 'duration']
	list_filter = ['duration']
	search_fields = ['title']

admin.site.register(models.Discipline, DiscliplineAdmin)
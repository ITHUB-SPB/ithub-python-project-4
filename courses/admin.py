from django.contrib import admin
from courses import models


class DiscliplineAdmin(admin.ModelAdmin):
	pass


admin.site.register(models.Discipline, DiscliplineAdmin)
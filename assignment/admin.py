from django.contrib import admin
from assignment import models

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['discipline__title', 'title', 'weight', 'updated_at']

admin.site.register(models.Assignment, AssignmentAdmin)
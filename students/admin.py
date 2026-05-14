from django.contrib import admin
from students import models


class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']
    list_filter = ['course']
    search_fields = ['title']


admin.site.register(models.Group, GroupAdmin)
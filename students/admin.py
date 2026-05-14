from django.contrib import admin
from students import models


class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']
    list_filter = ['course']
    search_fields = ['title']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'middle_name', 'account', 'group']
    list_filter = ['group']
    search_fields = ['last_name']


admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.Student, StudentAdmin)
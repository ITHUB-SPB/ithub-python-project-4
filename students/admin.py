from django.contrib import admin
from students import models


class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'course']
    list_filter = ['course']
    search_fields = ['title']
    list_editable = ['title', 'course']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'account', 'group']
    list_filter = ['group__title', 'group__course']
    search_fields = ['last_name', 'account__username']
    list_editable = ['group']


admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.Student, StudentAdmin)
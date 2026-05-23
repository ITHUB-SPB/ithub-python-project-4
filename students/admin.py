from django.contrib import admin
from students import models

@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
	list_display = ['title', 'year']
	list_filter = ['year']
	search_fields = ['title']


class StudentAdmin(admin.ModelAdmin):
	list_display = ['first_name', 'last_name', 'middle_name', 'account', 'group__title']
	list_filter = ['group__title', 'group__year']
	search_fields = ['last_name', 'account__username', 'account__email']


admin.site.register(models.Student, StudentAdmin)

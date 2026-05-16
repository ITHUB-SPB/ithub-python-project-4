from django.contrib import admin
from students import models


class StudentAdmin(admin.ModelAdmin):
	list_display = ['first_name', 'last_name', 'middle_name', 'account']
	search_fields = ['last_name', 'account__username', 'account__email']


admin.site.register(models.Student, StudentAdmin)

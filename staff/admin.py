from django.contrib import admin
from staff import models


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
	list_display = ['first_name', 'last_name', 'middle_name', 'account']
	search_fields = ['last_name', 'account__username', 'account__email']

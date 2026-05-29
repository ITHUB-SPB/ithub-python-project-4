from django.contrib import admin
from staff import models


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'account__username']


admin.site.register(models.Teacher, TeacherAdmin)
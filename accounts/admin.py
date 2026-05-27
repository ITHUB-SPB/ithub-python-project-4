from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from .models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = ['username', 'is_staff', 'is_superuser']
    list_filter = ['is_staff', 'is_superuser']
    search_fields = ['username']
    ordering = ['username']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Права', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
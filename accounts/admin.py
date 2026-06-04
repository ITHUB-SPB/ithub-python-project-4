from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from unfold.admin import ModelAdmin

from accounts import forms, models


admin.site.unregister(Group)


@admin.register(models.User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm
    change_password_form = forms.AdminPasswordChangeForm
    list_display = ["username", "is_active", "is_staff", "is_superuser"]
    list_filter = ["is_active", "is_staff", "is_superuser"]
    search_fields = ["username"]
    ordering = ["username"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Права", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Даты", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "is_active", "is_staff", "is_superuser"),
            },
        ),
    )


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

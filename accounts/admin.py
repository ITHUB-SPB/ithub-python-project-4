from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from unfold.admin import ModelAdmin

from accounts import forms, models


try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass


@admin.register(models.User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm
    change_password_form = forms.AdminPasswordChangeForm
    list_display = ("username", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "groups")
    search_fields = ("username",)
    ordering = ("username",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Права доступа", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "is_staff", "is_superuser"),
            },
        ),
    )


@admin.register(Group)
class AuthGroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

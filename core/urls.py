from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("accounts.urls")),   # ← для логина/логаута
    path("courses/", include("students.urls")), # ← для курсов
]

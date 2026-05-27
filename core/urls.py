from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="accounts:login")),
    path("admin/", admin.site.urls),
    path("auth/", include("accounts.urls")),
    path("courses/", include("courses.urls")),
]

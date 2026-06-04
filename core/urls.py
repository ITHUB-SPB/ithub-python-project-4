from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("accounts.urls")),
    path("courses/", include("courses.urls")),
    path("topics/", include("courses.topic_urls")),
]

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


urlpatterns = [
    path("", lambda request: redirect("/courses")),
    path("admin/", admin.site.urls),
    path("auth/", include("accounts.urls")),
    path("", include("courses.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('assignments/', include('assignment.urls')),
    path('auth/', include('students.urls'))
]

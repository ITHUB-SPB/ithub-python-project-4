from django.contrib import admin
from django.urls import path
from accounts import views as account_views
from courses import views as course_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/login", account_views.login_view, name="login"),
    path("auth/logout", account_views.logout_view, name="logout"),
    path("courses", course_views.courses_list_view, name="courses_list"),
    path("courses/<int:id>", course_views.course_detail_view, name="course_detail"),
]

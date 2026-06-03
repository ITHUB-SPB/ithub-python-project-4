from django.contrib import admin
from django.urls import path
from accounts.views import login_view, logout_view
from courses.views import course_detail_view, courses_list_view, topic_detail_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/login", login_view, name="login"),
    path("auth/logout", logout_view, name="logout"),
    path("courses", courses_list_view, name="courses-list"),
    path("courses/<int:course_id>", course_detail_view, name="course-detail"),
    path("topics/<int:topic_id>", topic_detail_view, name="topic-detail"),
]

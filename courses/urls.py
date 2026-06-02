from django.urls import path

from courses import views


urlpatterns = [
    path("", views.courses_list_view, name="courses_list"),
    path("<int:id>", views.course_detail_view, name="course_detail"),
    path("topics/<int:topic_id>", views.topic_detail_view, name="topic_detail"),
]

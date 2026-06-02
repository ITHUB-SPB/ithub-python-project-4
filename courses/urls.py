from django.urls import path

from courses import views


app_name = "courses"

urlpatterns = [
    path("courses", views.course_list_view, name="list"),
    path("courses/<int:course_id>", views.course_detail_view, name="detail"),
    path("topics/<int:topic_id>", views.topic_detail_view, name="topic-detail"),
]

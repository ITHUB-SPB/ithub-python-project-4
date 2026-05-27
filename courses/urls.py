from django.urls import path
from . import views 

app_name = "courses"

urlpatterns = [
    path("", views.CourseListView.as_view(), name="list"),
    path("<int:pk>/", views.CourseDetailView.as_view(), name="detail"),
    path("topics/<int:pk>/", views.TopicDetailView.as_view(), name="topic_detail"),
    path("assignments/<int:pk>/", views.AssignmentView.as_view(), name="assignment"),
    path("api/courses/", views.CourseListAPIView.as_view(), name="api_course_list"),
]
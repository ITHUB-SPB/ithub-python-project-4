from django.urls import path
from courses import views

urlpatterns = [
    path('', views.index, name="courses"),
    path('<int:course_id>', views.detail, name="course"),
    path('topics/<int:topic_id>', views.topic, name="topic"),
    path('submission/<int:assignment_id>', views.submission, name="submission")
]

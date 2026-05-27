from django.urls import path
from . import views

urlpatterns = [
    path("", views.courses_list, name="courses_list"),           # /courses/
    path("<int:course_id>/", views.course_detail, name="course_detail"),  # /courses/:id
]
from django.urls import path

from courses.views import course_detail, course_list


app_name = "courses"

urlpatterns = [
    path("", course_list, name="list"),
    path("<int:course_id>", course_detail, name="detail"),
]

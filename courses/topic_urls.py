from django.urls import path

from courses.views import topic_detail


app_name = "topics"

urlpatterns = [
    path("<int:topic_id>", topic_detail, name="detail"),
]

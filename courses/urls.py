from django.urls import path

from .views import course_list, course_detail, topic_detail

urlpatterns = [
    path('', course_list),
    path('<int:id>', course_detail),
    path('topics/<int:topic_id>/', topic_detail, name='topic_detail'),
]
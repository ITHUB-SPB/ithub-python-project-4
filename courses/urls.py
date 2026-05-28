from django.urls import path
from courses import views

urlpatterns = [
    path('', views.index, name='courses_list'),
    path('<int:course_id>', views.detail, name='course_detail'),
    path('<int:course_id>/topics/<int:topic_id>', views.topic, name='topic'),
]

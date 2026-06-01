from django.urls import path
from courses import views
from staff import views as staff_views

urlpatterns = [
    path('', views.index, name='courses'),
    path('', staff_views.index, name='staff'),
    path('<int:course_id>/', views.detail, name='course_detail'),
    path('<int:course_id>/<int:topic_id>/', views.topic, name='topic'),
    path('<int:course_id>/<int:topic_id>/<int:assignment_id>/', views.assignment, name='assignment'),
    path('<int:course_id>/<int:topic_id>/<int:assignment_id>/submission/', views.submission, name='submission'),
]
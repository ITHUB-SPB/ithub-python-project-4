from django.urls import path
from . import views

app_name = 'topics'
urlpatterns = [
    path('<int:topic_id>/', views.topic_detail, name='detail'),
    path('<int:topic_id>/submit/', views.submit_answer, name='submit'),
]
from django.urls import path
from courses import views

urlpatterns = [
    path('', views.index, name='courses_list'),
    path('<int:course_id>', views.detail, name='course_detail'),
]

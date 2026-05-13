from django.urls import path
from courses import views

urlpatterns = [
    path('', views.index, name="courses"),
    path('<int:id>', views.detail, name="course"),
]

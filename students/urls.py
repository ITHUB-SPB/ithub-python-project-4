from django.urls import include, path
from students import views
from staff import views as staff_views
from courses import views as courses_views

urlpatterns = [
    path('staff', include('staff.urls')),
    path('courses', include('courses.urls')),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]
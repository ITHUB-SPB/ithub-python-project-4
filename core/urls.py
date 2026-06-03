from django.contrib import admin
from django.urls import path
from accounts.views import login_view, logout_view
from courses.views import course_list, course_detail, topic_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('courses/', course_list, name='course_list'),
    path('courses/<int:id>/', course_detail, name='course_detail'),
    path('topics/<int:topic_id>/', topic_detail, name='topic_detail'),
]
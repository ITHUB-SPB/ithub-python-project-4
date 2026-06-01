from django.urls import path
from staff import views

urlpatterns = [
    path('admin/', views.index, name='staff'),
    path('admin/students/', views.students, name='students'),
    path('admin/teachers/', views.teachers, name='teachers'),
    path('admin/groups/', views.groups, name='groups'),
    path('admin/disciplines/', views.disciplines, name='disciplines'),
    path('admin/courses/', views.courses, name='courses'),
    path('admin/courses/<int:course_id>/topics/', views.topics, name='topics'),
    path('admin/courses/<int:course_id>/topics/<int:topic_id>/assignments/<int:assignment_id>/', views.assignment, name='assignment')
]
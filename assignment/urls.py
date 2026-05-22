from django.urls import path
from assignment import views

urlpatterns = [
    path('<int:assignment_id>', views.index, name='assignment')
]

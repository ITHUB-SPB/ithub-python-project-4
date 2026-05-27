from django.shortcuts import render, get_object_or_404
from .models import Course

def courses_list(request):
    courses = Course.objects.select_related('discipline', 'group').all()
    return render(request, 'courses/list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course.objects.select_related('discipline', 'group', 'teacher'), id=course_id)
    return render(request, 'courses/detail.html', {'course': course})
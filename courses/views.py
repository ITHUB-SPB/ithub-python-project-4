from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course
from students.models import Student


@login_required(login_url="/auth/login/")
def course_list(request):
    try:
        student = request.user.student
        courses = Course.objects.filter(group=student.group)
    except Student.DoesNotExist:
        courses = Course.objects.none()

    return render(request, "courses/course_list.html", {"courses": courses})


@login_required(login_url="/auth/login/")
def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, "courses/course_detail.html", {"course": course})

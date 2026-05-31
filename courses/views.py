from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from courses.models import Course


@login_required(login_url="/auth/login")
def courses_list_view(request):
    student = request.user.student
    courses = Course.objects.filter(group=student.group).select_related("discipline", "teacher", "group")
    return render(request, "courses/list.html", {"courses": courses})


@login_required(login_url="/auth/login")
def course_detail_view(request, id):
    student = request.user.student
    course = get_object_or_404(Course.objects.select_related("discipline", "teacher", "group"), id=id, group=student.group)
    return render(request, "courses/detail.html", {"course": course})

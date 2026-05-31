from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from courses.models import Course
from students.models import Student


@login_required(login_url="/auth/login")
def courses_list_view(request):
    student = Student.objects.filter(account=request.user).select_related("group").first()
    courses = Course.objects.none()

    if student and student.group:
        courses = Course.objects.filter(group=student.group).select_related("discipline", "teacher")

    return render(request, "courses/list.html", {"courses": courses})


@login_required(login_url="/auth/login")
def course_detail_view(request, course_id):
    student = Student.objects.filter(account=request.user).select_related("group").first()
    if student and student.group:
        course = get_object_or_404(Course, id=course_id, group=student.group)
        return render(request, "courses/detail.html", {"course": course})
    return render(request, "courses/detail.html", {"course": None})

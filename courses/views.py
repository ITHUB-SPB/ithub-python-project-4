from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from courses.models import Course
from students.models import Student


@login_required(login_url=reverse_lazy('login'))
def index(request):
    student = Student.objects.select_related('group').filter(account=request.user).first()

    if student is None:
        messages.error(request, 'К этому аккаунту не привязан студент')
        auth_logout(request)
        return redirect('login')

    courses = Course.objects.select_related(
        'discipline',
        'group',
        'teacher'
    ).filter(
        group=student.group
    )

    return render(
        request,
        'index.html',
        {
            'courses': courses,
            'student': student,
        }
    )


@login_required(login_url=reverse_lazy('login'))
def detail(request, course_id):
    student = Student.objects.select_related('group').filter(account=request.user).first()

    if student is None:
        messages.error(request, 'К этому аккаунту не привязан студент')
        auth_logout(request)
        return redirect('login')

    course = get_object_or_404(
        Course.objects.select_related('discipline', 'group', 'teacher'),
        pk=course_id,
        group=student.group
    )

    return render(
        request,
        'course.html',
        {
            'course': course,
            'student': student,
        }
    )
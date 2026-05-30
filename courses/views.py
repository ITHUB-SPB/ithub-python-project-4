from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from students.models import Student
from .models import Course


@login_required(login_url='/auth/login')
def course_list(request):
    student = Student.objects.get(
        account=request.user
    )

    courses = Course.objects.filter(
        group=student.group
    )

    return render(
        request,
        'courses/list.html',
        {'courses': courses}
    )
    

@login_required(login_url='/auth/login')
def course_detail(request, id):
    course = get_object_or_404(
        Course,
        pk=id
    )

    return render(
        request,
        'courses/detail.html',
        {'course': course}
    )
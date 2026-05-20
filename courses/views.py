from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from courses import models
from students import models as students_models

@login_required(login_url='/accounts/login')
def index(request):
    all_courses = models.Course.objects.filter(group=request.user.student.group)

    return render(request, 'all_courses.html', {
        "courses": all_courses
    })


@login_required(login_url='/accounts/login')
def detail(request, id):
    course = models.Course.objects.get(pk=id)

    return render(request, 'course.html', {
        "course": course
    })
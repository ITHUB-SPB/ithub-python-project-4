from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from courses import models


def index(request):
    all_courses = models.Course.objects.all()

    return render(request, 'all_courses.html', {
        "courses": all_courses
    })


def detail(request, id):
    course = models.Course.objects.get(pk=id)

    return render(request, 'course.html', {
        "course": course
    })
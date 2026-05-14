from django.shortcuts import render
from courses import models


def index(request):
    disciplines = models.Disclipline.objects.all()

    return render(
        request,
        'index.html',
        { 'disciplines': disciplines }
    )


def detail(request, course_id):
    discipline = models.Disclipline.objects.get(pk=course_id)

    return render(
        request,
        'course.html',
        { 'discipline': discipline }
    )

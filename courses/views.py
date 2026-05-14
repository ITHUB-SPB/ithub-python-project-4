from django.shortcuts import render
from courses import models

def index(request):
    courses = models.Discipline.objects.all()

    return render(
        request,
        'courses.html',
        { 'courses': courses }
    )


def detail(request, course_id):
    course = models.Discipline.objects.get(pk=course_id)

    return render(
        request,
        'course.html',
        { 'course': course }
    )
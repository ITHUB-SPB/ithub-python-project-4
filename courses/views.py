from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render
from courses import models


@login_required(login_url=reverse_lazy('login'))
def index(request):
    disciplines = models.Course.objects.filter(group=request.user.student.group)

    return render(
        request,
        'index.html',
        { 'disciplines': disciplines }
    )


@login_required(login_url=reverse_lazy('login'))
def detail(request, course_id):
    discipline = models.Disclipline.objects.get(pk=course_id)

    return render(
        request,
        'course.html',
        { 'discipline': discipline }
    )

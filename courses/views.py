from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from courses import models
from courses.models import Submission


@login_required(login_url=reverse_lazy('login'))
def index(request):
    courses = models.Course.objects.filter(group=request.user.student.group)

    return render(
        request,
        'index.html',
        { 'courses': courses }
    )


@login_required(login_url=reverse_lazy('login'))
def detail(request, course_id):
    course = models.Course.objects.get(pk=course_id)

    return render(
        request,
        'course.html',
        { 'course': course }
    )


@login_required(login_url=reverse_lazy('login'))
def topic(request, topic_id):
    topic = models.Topic.objects.get(pk=topic_id)

    return render(
        request,
        'topic.html',
        { 'topic': topic }
    )


@login_required(login_url=reverse_lazy('login'))
def submission(request, assignment_id):
    assignment = models.Assignment.objects.get(pk=assignment_id)
    student = request.user.student
    answer = request.POST.get('answer')

    Submission(
        assignment=assignment,
        student=student,
        answer=answer,
        score=0
    ).save()

    return redirect(reverse('courses'))

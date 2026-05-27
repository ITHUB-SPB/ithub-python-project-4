from django.contrib import messages
from django.shortcuts import render, redirect, reverse
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


@login_required(login_url='/accounts/login')
def topic(request, topic_id):
    topic = models.Topic.objects.get(pk=topic_id)

    return render(request, 'topic.html', {
        "topic": topic
    })


@login_required(login_url='/accounts/login')
def submission(request, assignment_id):
    answer = request.POST.get('answer')
    assignment = models.Assignment.objects.get(pk=assignment_id)
    student = request.user.student

    models.Submission(answer=answer, assignment=assignment, student=student).save()

    messages.success(request, message='Ответ отправлен!')

    return redirect(reverse(
        'topic',
        kwargs={
            'topic_id': assignment.topic.id
        }
    ))
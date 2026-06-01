from django.shortcuts import render, redirect
from courses import models
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.contrib import messages

# Create your views here.
@login_required(login_url=reverse_lazy('login'))
def index(request):
    if request.user.is_staff:
        return render(request, 'admin_panel.html')

    group = request.user.student.group
    student = request.user.student
    courses = models.Course.objects.filter(group=group)
    
    scores = {}
    for course in courses:    
        student_score = models.Submission.objects.filter(student=student, assignment__topic__discipline__course=course).values('score')
        scores[course.id] = sum(item['score'] for item in student_score)

    return render(request, 'courses.html', { 'courses': courses, 'scores': scores })

@login_required(login_url=reverse_lazy('login'))
def detail(request, course_id):    
    course = models.Course.objects.get(pk=course_id)
    topics = course.discipline.topic_set.all()
    scores = {}

    for topic in topics:
        if hasattr(topic, 'assignment') and topic.assignment:
            scores[topic.id] = models.Submission.objects.filter(
                student=request.user.student,
                assignment=topic.assignment
            ).values_list('score', flat=True).first()
        else:
            topic.submission = None

    print(scores)

    return render(request, 'course_detail.html', { 'course': course, 'scores': scores })

@login_required(login_url=reverse_lazy('login'))
def topic(request, course_id, topic_id):
    topic = models.Topic.objects.get(pk=topic_id)
    course = models.Course.objects.get(pk=course_id)

    submission = models.Submission.objects.filter(
        student=request.user.student,
        assignment=topic.assignment
    ).first()

    if request.method == 'POST' and submission is None:
        models.Submission(
            student=request.user.student,
            assignment=topic.assignment,
            answer=request.POST.get('answer'),
        ).save()
        messages.success(request, 'Ответ успешно сохранён!')
        return redirect('topic', course_id=course_id, topic_id=topic_id)

    return render(request, 'topic.html', { 'topic': topic, 'course': course, 'submission': submission })

@login_required(login_url=reverse_lazy('login'))
def assignment(request, topic_id, assignment_id):
    assignment = models.Assignment.objects.get(pk=assignment_id)
    topic = models.Topic.objects.get(pk=topic_id)
    discipline = topic.discipline
    return render(request, 'assignment.html', { 'assignment': assignment, 'topic': topic, 'discipline': discipline })

@login_required(login_url=reverse_lazy('login'))
def submission(request, topic_id, assignment_id):
    assignment = models.Assignment.objects.get(pk=assignment_id)
    topic = models.Topic.objects.get(pk=topic_id)
    discipline = topic.discipline
    return render(request, 'submission.html', { 'assignment': assignment, 'topic': topic, 'discipline': discipline })
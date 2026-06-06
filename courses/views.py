from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from students.models import Student
from assignments.models import Assignment, Submission
from .models import Course
from courses.models import Topic


@login_required(login_url='/auth/login')
def course_list(request):
    student = Student.objects.get(account=request.user)
    courses = Course.objects.filter(group=student.group)

    courses_data = []

    for course in courses:
        assignment = Assignment.objects.filter(
            topic__discipline=course.discipline
        ).first()

        score = None

        if assignment:
            submission = Submission.objects.filter(
                student=student,
                assignment=assignment
            ).first()

            if submission:
                score = submission.score

        courses_data.append({
            'course': course,
            'assignment': assignment,
            'score': score,
        })

    return render(
        request,
        'courses/list.html',
        {
            'courses_data': courses_data
        }
    )


@login_required(login_url='/auth/login')
def course_detail(request, id):
    course = get_object_or_404(Course, pk=id)
    student = Student.objects.get(account=request.user)
    topics = Topic.objects.filter(discipline=course.discipline)

    topics_data = []

    for topic in topics:
        assignment = Assignment.objects.filter(
            topic=topic
        ).first()

        score = None

        if assignment:
            submission = Submission.objects.filter(
                student=student,
                assignment=assignment
            ).first()

            if submission:
                score = submission.score

        topics_data.append({
            'topic': topic,
            'assignment': assignment,
            'score': score,
        })

    return render(
        request,
        'courses/detail.html',
        {
            'course': course,
            'topics_data': topics_data,
        }
    )
    
@login_required(login_url='/auth/login')
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    student = Student.objects.get(account=request.user)

    assignment = Assignment.objects.filter(
        topic=topic
    ).first()

    submission = None

    if assignment:
        submission = Submission.objects.filter(
            student=student,
            assignment=assignment
        ).first()

    if request.method == 'POST' and assignment and not submission:
        answer = request.POST.get('answer')

        Submission.objects.create(
            student=student,
            assignment=assignment,
            answer=answer,
        )

        messages.success(
            request,
            'Ответ успешно отправлен'
        )

        return redirect(
            'topic_detail',
            topic_id=topic.id
        )

    return render(
        request,
        'courses/topic.html',
        {
            'topic': topic,
            'assignment': assignment,
            'submission': submission,
        }
    )
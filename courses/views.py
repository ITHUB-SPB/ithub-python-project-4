from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from assignments.forms import SubmissionForm
from assignments.models import Submission
from courses.models import Course, Topic
from students.models import Student


def get_student(request):
    return Student.objects.filter(account=request.user).select_related("group").first()


def get_assignment(topic):
    if hasattr(topic, "assignment"):
        return topic.assignment
    return None


def get_course_score(course, student):
    current_score = 0
    max_score = 0

    if not course.discipline:
        return current_score, max_score

    topics = Topic.objects.filter(discipline=course.discipline).order_by("ordering_number")

    for topic in topics:
        assignment = get_assignment(topic)
        if assignment:
            max_score += assignment.weight
            submission = Submission.objects.filter(assignment=assignment, student=student).first()
            if submission and submission.score is not None:
                current_score += submission.score

    return current_score, max_score


@login_required(login_url="/auth/login")
def courses_list_view(request):
    student = get_student(request)
    courses = Course.objects.none()

    if student and student.group:
        courses = Course.objects.filter(group=student.group).select_related("discipline", "teacher")
        for course in courses:
            course.current_score, course.max_score = get_course_score(course, student)

    return render(request, "courses/list.html", {"courses": courses})


@login_required(login_url="/auth/login")
def course_detail_view(request, course_id):
    student = get_student(request)
    if student and student.group:
        course = get_object_or_404(Course, id=course_id, group=student.group)
        topics = Topic.objects.filter(discipline=course.discipline).order_by("ordering_number")
        for topic in topics:
            topic.assignment_item = get_assignment(topic)
            topic.submission = None
            topic.has_score = False
            if topic.assignment_item:
                topic.submission = Submission.objects.filter(
                    assignment=topic.assignment_item,
                    student=student,
                ).first()
                if topic.submission and topic.submission.score is not None:
                    topic.has_score = True
        return render(request, "courses/detail.html", {"course": course, "topics": topics})
    return render(request, "courses/detail.html", {"course": None})


@login_required(login_url="/auth/login")
def topic_detail_view(request, topic_id):
    student = get_student(request)
    if not student or not student.group:
        raise Http404

    topic = get_object_or_404(Topic, id=topic_id)
    course = (
        Course.objects.filter(group=student.group, discipline=topic.discipline)
        .select_related("discipline", "teacher", "group")
        .first()
    )

    if not course:
        raise Http404

    assignment = get_assignment(topic)
    submission = None

    if assignment:
        submission = Submission.objects.filter(assignment=assignment, student=student).first()
        has_score = submission is not None and submission.score is not None
    else:
        has_score = False

    if request.method == "POST" and assignment and not submission:
        form = SubmissionForm(request.POST)
        if form.is_valid():
            new_submission = form.save(commit=False)
            new_submission.student = student
            new_submission.assignment = assignment
            new_submission.score = None
            new_submission.save()
            messages.success(request, "Ответ успешно отправлен")
            return redirect("topic-detail", topic_id=topic.id)
    else:
        form = SubmissionForm()

    context = {
        "course": course,
        "topic": topic,
        "assignment": assignment,
        "submission": submission,
        "has_score": has_score,
        "form": form,
    }
    return render(request, "courses/topic_detail.html", context)

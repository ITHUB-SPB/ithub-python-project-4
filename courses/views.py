from dataclasses import dataclass

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from courses.forms import SubmissionForm
from courses.models import ControlPoint, Course, Submission, Topic
from students.models import Student


@dataclass
class TopicProgress:
    topic: Topic
    control_point: ControlPoint | None
    submission: Submission | None

    @property
    def earned_score(self):
        if self.submission is None or self.submission.score is None:
            return None
        return self.submission.score

    @property
    def max_score(self):
        if self.control_point is None:
            return None
        return self.control_point.max_score

    @property
    def status(self):
        if self.control_point is None:
            return "Тема"
        if self.submission is None:
            return "Не сдано"
        if self.submission.score is None:
            return "На проверке"
        return "Сдано"


def get_control_point(topic: Topic):
    try:
        return topic.control_point
    except ControlPoint.DoesNotExist:
        return None


def get_student_for_user(user) -> Student:
    student = getattr(user, "student", None)
    if student is None:
        raise PermissionDenied
    return student


def get_course_for_student(student: Student, course_id: int) -> Course:
    return get_object_or_404(
        Course.objects.select_related("discipline", "teacher", "group"),
        id=course_id,
        group=student.group,
    )


def get_course_for_topic(student: Student, topic: Topic) -> Course:
    course = (
        Course.objects.select_related("discipline", "teacher", "group")
        .filter(group=student.group, discipline=topic.discipline)
        .first()
    )
    if course is None:
        raise Http404
    return course


def build_topic_progress(course: Course, student: Student):
    topics = course.discipline.topics.select_related("control_point").all() if course.discipline else []
    submission_map = {
        submission.control_point_id: submission
        for submission in Submission.objects.filter(course=course, student=student).select_related("control_point")
    }
    progress_items = []
    for topic in topics:
        control_point = get_control_point(topic)
        submission = submission_map.get(control_point.id) if control_point is not None else None
        progress_items.append(TopicProgress(topic=topic, control_point=control_point, submission=submission))
    return progress_items


def grade_from_scores(earned_score: int, max_score: int):
    if max_score <= 0:
        return None
    ratio = earned_score / max_score
    if ratio >= 0.85:
        return 5
    if ratio >= 0.7:
        return 4
    if ratio >= 0.5:
        return 3
    return 2


@login_required(login_url="/auth/login")
def course_list_view(request: HttpRequest) -> HttpResponse:
    student = get_student_for_user(request.user)
    courses = (
        Course.objects.filter(group=student.group)
        .select_related("discipline", "teacher", "group")
        .prefetch_related("discipline__topics__control_point__submissions")
    )
    items = []
    for course in courses:
        max_score = 0
        earned_score = 0
        if course.discipline is not None:
            for topic in course.discipline.topics.all():
                control_point = get_control_point(topic)
                if control_point is None:
                    continue
                max_score += control_point.max_score
                submission = next(
                    (
                        submission
                        for submission in control_point.submissions.all()
                        if submission.course_id == course.id and submission.student_id == student.id
                    ),
                    None,
                )
                if submission is not None and submission.score is not None:
                    earned_score += submission.score
        items.append(
            {
                "course": course,
                "earned_score": earned_score,
                "max_score": max_score,
                "grade": grade_from_scores(earned_score, max_score),
            }
        )
    return render(request, "courses/course_list.html", {"student": student, "items": items})


@login_required(login_url="/auth/login")
def course_detail_view(request: HttpRequest, course_id: int) -> HttpResponse:
    student = get_student_for_user(request.user)
    course = get_course_for_student(student, course_id)
    topic_items = build_topic_progress(course, student)
    max_score = sum(item.max_score or 0 for item in topic_items)
    return render(
        request,
        "courses/course_detail.html",
        {
            "student": student,
            "course": course,
            "topic_items": topic_items,
            "discipline_hours": course.discipline.duration if course.discipline else 0,
            "max_score": max_score,
        },
    )


@login_required(login_url="/auth/login")
def topic_detail_view(request: HttpRequest, topic_id: int) -> HttpResponse:
    student = get_student_for_user(request.user)
    topic = get_object_or_404(Topic.objects.select_related("discipline"), id=topic_id)
    course = get_course_for_topic(student, topic)
    control_point = get_control_point(topic)
    if control_point is None:
        return render(
            request,
            "courses/topic_detail.html",
            {
                "student": student,
                "course": course,
                "topic": topic,
            },
        )

    submission = (
        Submission.objects.filter(course=course, control_point=control_point, student=student)
        .select_related("control_point", "course", "student")
        .first()
    )
    if request.method == "POST" and submission is None:
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.course = course
            submission.control_point = control_point
            submission.student = student
            submission.save()
            messages.success(request, "Ответ успешно отправлен.")
            return redirect("courses:topic-detail", topic_id=topic.id)
    else:
        form = SubmissionForm()
    return render(
        request,
        "courses/control_point_detail.html",
        {
            "student": student,
            "course": course,
            "topic": topic,
            "control_point": control_point,
            "submission": submission,
            "form": form,
        },
    )

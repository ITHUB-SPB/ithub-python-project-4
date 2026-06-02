from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Assignment, Course, Submission, Topic


def get_student(request):
    return request.user.student


@login_required(login_url="/auth/login")
def courses_list_view(request):
    student = get_student(request)
    courses = list(
        Course.objects.filter(group=student.group).select_related("discipline", "teacher", "group")
    )

    for course in courses:
        if course.discipline_id:
            assignments = Assignment.objects.filter(topic__discipline=course.discipline).select_related("topic")
            total_score = (
                Submission.objects.filter(student=student, assignment__topic__discipline=course.discipline).aggregate(total=Sum("score"))["total"]
                or 0
            )
            course.total_points = sum(assignment.weight for assignment in assignments)
            course.total_score = total_score
        else:
            course.total_points = 0
            course.total_score = 0

    return render(request, "courses/list.html", {"courses": courses})


@login_required(login_url="/auth/login")
def course_detail_view(request, id):
    student = get_student(request)
    course = get_object_or_404(Course.objects.select_related("discipline", "teacher", "group"), id=id, group=student.group)
    topics = []

    if course.discipline_id:
        topics = list(
            Topic.objects.filter(discipline=course.discipline).select_related("discipline").order_by("ordering_number")
        )

        for topic in topics:
            topic.student_submission = None
            if hasattr(topic, "assignment"):
                topic.student_submission = Submission.objects.filter(student=student, assignment=topic.assignment).first()

    return render(request, "courses/detail.html", {"course": course, "topics": topics})


@login_required(login_url="/auth/login")
def topic_detail_view(request, topic_id):
    student = get_student(request)
    topic = get_object_or_404(
        Topic.objects.select_related("discipline").filter(discipline__course__group=student.group).distinct(),
        id=topic_id,
    )
    submission = None
    assignment = getattr(topic, "assignment", None)

    if assignment:
        submission = Submission.objects.filter(student=student, assignment=assignment).first()

        if request.method == "POST" and submission is None:
            answer = request.POST.get("answer", "").strip()
            if answer:
                Submission.objects.create(student=student, assignment=assignment, answer=answer)
                messages.success(request, "Ответ отправлен")
                return redirect("topic_detail", topic_id=topic.id)
            messages.error(request, "Введите ответ")

    return render(
        request,
        "courses/topic.html",
        {"topic": topic, "assignment": assignment, "submission": submission},
    )

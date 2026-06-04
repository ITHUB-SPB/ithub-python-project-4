from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from assignments.models import Assignment, Submission
from courses.forms import SubmissionForm
from courses.models import Course, Topic
from students.models import Student


def get_student(request):
    return get_object_or_404(Student.objects.select_related("group"), account=request.user)


@login_required(login_url="/auth/login")
def course_list(request):
    student = get_student(request)
    courses = Course.objects.filter(group=student.group).select_related("discipline", "teacher", "group")
    rows = []
    for course in courses:
        assignments = Assignment.objects.filter(topic__discipline=course.discipline).select_related("topic")
        total_weight = assignments.aggregate(total=Sum("weight"))["total"] or 0
        submissions = Submission.objects.filter(student=student, assignment__in=assignments)
        total_score = submissions.aggregate(total=Sum("score"))["total"] or 0
        rows.append(
            {
                "course": course,
                "assignment_count": assignments.count(),
                "total_weight": total_weight,
                "total_score": total_score,
            }
        )
    return render(request, "courses/list.html", {"student": student, "rows": rows})


@login_required(login_url="/auth/login")
def course_detail(request, course_id):
    student = get_student(request)
    course = get_object_or_404(
        Course.objects.select_related("discipline", "teacher", "group"),
        id=course_id,
        group=student.group,
    )
    topics = Topic.objects.filter(discipline=course.discipline).select_related("discipline")
    items = []
    for topic in topics:
        assignment = Assignment.objects.filter(topic=topic).first()
        submission = None
        if assignment:
            submission = Submission.objects.filter(student=student, assignment=assignment).first()
        items.append({"topic": topic, "assignment": assignment, "submission": submission})
    return render(request, "courses/detail.html", {"course": course, "items": items})


@login_required(login_url="/auth/login")
def topic_detail(request, topic_id):
    student = get_student(request)
    topic = get_object_or_404(Topic.objects.select_related("discipline"), id=topic_id)
    if not Course.objects.filter(group=student.group, discipline=topic.discipline).exists():
        return redirect("courses:list")
    assignment = Assignment.objects.filter(topic=topic).first()
    submission = None
    if assignment:
        submission = Submission.objects.filter(student=student, assignment=assignment).first()
    form = SubmissionForm(request.POST or None)
    if assignment and submission is None and request.method == "POST" and form.is_valid():
        created_submission = form.save(commit=False)
        created_submission.student = student
        created_submission.assignment = assignment
        created_submission.save()
        messages.success(request, "Ответ успешно отправлен")
        return redirect("topics:detail", topic_id=topic.id)
    return render(
        request,
        "courses/topic.html",
        {"topic": topic, "assignment": assignment, "submission": submission, "form": form},
    )

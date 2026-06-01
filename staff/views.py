from datetime import date
from django.contrib import messages

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from numpy import number
from courses import models
from staff import models as staff_models
from django.shortcuts import redirect

# Create your views here.

@login_required(login_url=reverse_lazy('login'))
def index(request):
    user = request.user
    if not user.is_staff:
        return redirect('courses')

    return render(request, 'admin_panel.html')

def students(request):
    students = models.Student.objects.all()
    groups = models.Group.objects.all()
    if not request.user.is_superuser:
        students = students.filter(
            group__course__teacher=request.user.teacher
        )

    group_id = request.GET.get('group')
    search = request.GET.get('search')

    if group_id:
        students = students.filter(group_id=group_id)

    if search:
        students = students.filter(
            last_name__icontains=search
        )

    students = students.distinct()
    return render(request, 'admin_students.html', {'students': students, 'groups': groups})

def teachers(request):
    if not request.user.is_superuser:
        return redirect('staff')
    teachers = models.Teacher.objects.all()

    search = request.GET.get('search')
    if search:
        teachers = teachers.filter(
            last_name__icontains=search
        )
    return render(request, 'admin_teachers.html', {'teachers': teachers} )

def groups(request):
    groups = models.Group.objects.all()

    year = request.GET.get('year')
    if year:
        groups = groups.filter(
            year=year
        )

    search = request.GET.get('search')
    if search:
        groups = groups.filter(
            title__icontains=search
        )
    return render(request, 'admin_groups.html', {'groups': groups})

def disciplines(request):
    disciplines = models.Discipline.objects.all()

    search = request.GET.get('search')
    if search:
        disciplines = disciplines.filter(
            title__icontains=search
        )
    return render(request, 'admin_disciplines.html', {'disciplines': disciplines})

def courses(request):
    courses = models.Course.objects.all()
    groups = models.Group.objects.all()
    teachers = models.Teacher.objects.all()
    periods = models.Course.objects.filter().values('course_start', 'course_end').distinct()

    if not request.user.is_staff:
        return redirect('courses')
    if not request.user.is_superuser:
        courses = courses.filter(teacher=request.user.teacher)

    group = request.GET.get('group')
    if group:
        courses = courses.filter(group_id=group)
    teacher = request.GET.get('teacher')
    if teacher:
        courses = courses.filter(teacher_id=teacher)
    year = request.GET.get('year')
    if year:
        courses = courses.filter(group__year=year)

    return render(request, 'admin_courses.html', {'courses': courses, 'groups': groups, 'teachers': teachers, 'periods': periods})

@login_required(login_url=reverse_lazy('login'))
def topics(request, course_id):
    course = models.Course.objects.get(pk=course_id)
    topics = course.discipline.topic_set.all()
    return render(request, 'admin_topics.html', { 'course': course, 'topics': topics })

@login_required(login_url=reverse_lazy('login'))
def assignment(request, course_id, topic_id, assignment_id):
    course = models.Course.objects.get(pk=course_id)
    topic = course.discipline.topic_set.get(pk=topic_id)
    assignment = topic.assignment
    submissions = assignment.submission_set.all()

    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        score = request.POST.get('score')
        if score == '':
            score = None
        else:
            if int(score) > assignment.weight:
                messages.error(request, 'Оценка не может быть больше максимальной')
                return redirect(
                    'assignment',
                    course_id=course_id,
                    topic_id=topic_id,
                    assignment_id=assignment_id
                )
            if int(score) < 0:
                messages.error(request, 'Оценка не может быть меньше 0')
                return redirect(
                    'assignment',
                    course_id=course_id,
                    topic_id=topic_id,
                    assignment_id=assignment_id
                )

        models.Submission.objects.filter(
            pk=submission_id,
            assignment=assignment
        ).update(score=score)
        submission = models.Submission.objects.get(
            pk=submission_id,
            assignment=assignment
        )
        submission.save()

        return redirect(
            'assignment',
            course_id=course_id,
            topic_id=topic_id,
            assignment_id=assignment_id
        )

    return render(request, 'admin_assignment.html', { 'course': course, 'topic': topic, 'assignment': assignment, 'submissions': submissions })
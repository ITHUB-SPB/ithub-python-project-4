from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Topic, ControlPoint
from students.models import Student


@login_required(login_url='/auth/login/')
def course_list(request):
    try:
        student = Student.objects.get(account=request.user)
        courses = Course.objects.filter(group=student.group)
    except Student.DoesNotExist:
        courses = Course.objects.none()
        messages.warning(request, 'Ваш аккаунт не привязан к студенту')
    
    return render(request, 'courses/course_list.html', {'courses': courses})


@login_required(login_url='/auth/login/')
def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    
    try:
        student = Student.objects.get(account=request.user)
        if course.group != student.group:
            messages.error(request, 'У вас нет доступа к этому курсу')
            return redirect('course_list')
    except Student.DoesNotExist:
        messages.error(request, 'Студент не найден')
        return redirect('course_list')
    
    topics = Topic.objects.filter(course=course)
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'topics': topics
    })


@login_required(login_url='/auth/login/')
def topic_detail(request, course_id, topic_id):
    course = get_object_or_404(Course, id=course_id)
    topic = get_object_or_404(Topic, id=topic_id, course=course)
    
    # Проверка доступа
    try:
        student = Student.objects.get(account=request.user)
        if course.group != student.group:
            messages.error(request, 'У вас нет доступа')
            return redirect('course_list')
    except Student.DoesNotExist:
        messages.error(request, 'Студент не найден')
        return redirect('course_list')
    
    control_points = ControlPoint.objects.filter(topic=topic)
    
    return render(request, 'courses/topic_detail.html', {
        'course': course,
        'topic': topic,
        'control_points': control_points
    })
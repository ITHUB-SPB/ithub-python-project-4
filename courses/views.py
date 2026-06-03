from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course
from students.models import Student
from staff.models import Teacher

def get_user_role(user):
    if hasattr(user, 'student'):
        return 'student'
    elif hasattr(user, 'teacher'):
        return 'teacher'
    elif hasattr(user, 'manager'):
        return 'manager'
    return None

@login_required(login_url='login')
def course_list(request):
    user = request.user
    
    if hasattr(user, 'student'):
        student = user.student
        if student.group:
            courses = Course.objects.filter(group=student.group)
        else:
            courses = Course.objects.none()
            messages.warning(request, 'Вы не прикреплены к группе')
        template = 'courses/course_list.html'
        
    elif hasattr(user, 'teacher'):
        teacher = user.teacher
        courses = Course.objects.filter(teacher=teacher)
        template = 'courses/course_list.html'
        
    elif hasattr(user, 'manager'):
        courses = Course.objects.all()
        template = 'courses/course_list.html'
        
    else:
        messages.error(request, 'Неизвестная роль пользователя')
        return redirect('login')
    
    return render(request, template, {'courses': courses})


@login_required(login_url='login')
def course_detail(request, id):
    user = request.user
    
    if hasattr(user, 'student'):
        student = user.student
        course = get_object_or_404(Course, id=id, group=student.group)
        
    elif hasattr(user, 'teacher'):
        teacher = user.teacher
        course = get_object_or_404(Course, id=id, teacher=teacher)
        
    elif hasattr(user, 'manager'):
        course = get_object_or_404(Course, id=id)
        
    else:
        messages.error(request, 'Неизвестная роль пользователя')
        return redirect('login')
    
    return render(request, 'courses/course_detail.html', {'course': course})
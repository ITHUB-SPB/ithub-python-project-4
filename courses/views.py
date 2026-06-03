from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Topic
from assignments.models import Assignment, Submission
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
        
        courses_with_score = []
        
        for course in courses:
            score_earned = 0
            score_max = 0

            for topic in course.discipline.topics.all():
                if hasattr(topic, 'assignment'):
                    submission = topic.assignment.submissions.filter(student=student).first()
            
                    if submission and submission.score is not None:
                        score_earned += submission.score
            
                    score_max += topic.assignment.weight
            
            courses_with_score.append({
                'course': course,
                'earned': score_earned,
                'max': score_max
            })
        
        template = 'courses/course_list.html'
        context = {'courses_with_score': courses_with_score}
    elif hasattr(user, 'teacher'):
        teacher = user.teacher
        courses = Course.objects.filter(teacher=teacher)
        template = 'courses/course_list.html'
        context = {'courses': courses}
    elif hasattr(user, 'manager'):
        courses = Course.objects.all()
        template = 'courses/course_list.html'
        context = {'courses': courses}
    else:
        messages.error(request, 'Неверная роль пользователя')
        return redirect('login')
    
    return render(request, template, context)


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
    
    topics = course.discipline.topics.all().prefetch_related('assignment__submissions')
    
    topics_with_score = []
    for topic in topics:
        topic_score = {'topic': topic, 'has_assignment': hasattr(topic, 'assignment')}
        
        if hasattr(user, 'student') and hasattr(topic, 'assignment'):
            submission = topic.assignment.submissions.filter(student=user.student).first()
            topic_score['submission'] = submission
            topic_score['max_score'] = topic.assignment.weight
        
        topics_with_score.append(topic_score)
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'topics_with_score': topics_with_score
    })


@login_required(login_url='login')
def topic_detail(request, topic_id):
    user = request.user
    topic = get_object_or_404(Topic, id=topic_id)
    
    course = None

    if hasattr(user, 'student'):
        student = user.student
    
        course = Course.objects.filter(
            discipline=topic.discipline, 
            group=student.group
        ).first()
    
        if not course:
            messages.error(request, 'У вас нет доступа к этому топику')
            return redirect('course_list')
    
    elif hasattr(user, 'teacher'):
        teacher = user.teacher
    
        course = Course.objects.filter(
            discipline=topic.discipline, 
            teacher=teacher
        ).first()
    
    elif hasattr(user, 'manager'):
        course = Course.objects.filter(
            discipline=topic.discipline
        ).first()
    
    has_assignment = hasattr(topic, 'assignment')
    submission = None
    
    if has_assignment and hasattr(user, 'student'):
        submission = topic.assignment.submissions.filter(student=user.student).first()
    
    return render(request, 'courses/topic_detail.html', {
        'topic': topic,
        'course': course,
        'has_assignment': has_assignment,
        'submission': submission,
        'assignment': topic.assignment if has_assignment else None
    })
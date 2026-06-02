from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Topic
from assignments.models import Submission
from assignments.forms import SubmissionForm   # ← добавить импорт
from students.models import Student

@login_required
def course_list(request):
    """Список курсов для студента"""
    try:
        student = request.user.student_profile
        courses = Course.objects.filter(group=student.group).select_related('discipline', 'teacher')
    except:
        return redirect('login')
    
    course_data = []
    for course in courses:
        topics = Topic.objects.filter(discipline=course.discipline)
        total_score = 0
        total_max = 0
        
        for topic in topics:
            if hasattr(topic, 'assignment'):
                try:
                    submission = Submission.objects.get(
                        student=student,
                        assignment=topic.assignment
                    )
                    if submission.score:
                        total_score += submission.score
                        total_max += topic.assignment.weight
                except Submission.DoesNotExist:
                    total_max += topic.assignment.weight
        
        grade = None
        if total_max > 0:
            percentage = (total_score / total_max) * 100
            if percentage >= 85:
                grade = 5
            elif percentage >= 70:
                grade = 4
            elif percentage >= 50:
                grade = 3
            else:
                grade = 2
        
        course_data.append({
            'course': course,
            'total_score': total_score,
            'total_max': total_max,
            'grade': grade
        })
    
    return render(request, 'courses/list.html', {'courses': course_data})


@login_required
def course_detail(request, course_id):
    """Детальная страница курса"""
    try:
        student = request.user.student_profile
    except:
        return redirect('login')
    
    course = get_object_or_404(Course, id=course_id, group=student.group)
    topics = Topic.objects.filter(
        discipline=course.discipline
    ).order_by('ordering_number')
    
    topic_data = []
    for topic in topics:
        topic_info = {
            'topic': topic,
            'has_assignment': hasattr(topic, 'assignment'),
            'score': None,
            'max_score': None,
            'duration': topic.duration,   # добавим, если нужно в шаблоне
        }
        
        if hasattr(topic, 'assignment'):
            topic_info['max_score'] = topic.assignment.weight
            try:
                submission = Submission.objects.get(
                    student=student,
                    assignment=topic.assignment
                )
                topic_info['score'] = submission.score
            except Submission.DoesNotExist:
                pass
        
        topic_data.append(topic_info)
    
    return render(request, 'courses/detail.html', {
        'course': course,
        'topics': topic_data
    })


@login_required
def topic_detail(request, topic_id):
    """Детальная страница топика"""
    try:
        student = request.user.student_profile
    except:
        return redirect('login')
    
    topic = get_object_or_404(Topic, id=topic_id)
    
    course = Course.objects.filter(
        group=student.group,
        discipline=topic.discipline
    ).first()
    
    if not course:
        return redirect('courses:list')
    
    context = {
        'topic': topic,
        'has_assignment': hasattr(topic, 'assignment'),
    }
    
    if hasattr(topic, 'assignment'):
        assignment = topic.assignment
        try:
            submission = Submission.objects.get(
                student=student,
                assignment=assignment
            )
            context['submission'] = submission
        except Submission.DoesNotExist:
            context['form'] = SubmissionForm()
    
    return render(request, 'courses/topic_detail.html', context)


@login_required
def submit_answer(request, topic_id):
    """Отправка ответа на контрольную точку"""
    if request.method != 'POST':
        return redirect('topics:detail', topic_id=topic_id)  # исправлено
    
    topic = get_object_or_404(Topic, id=topic_id)
    student = request.user.student_profile
    
    if not hasattr(topic, 'assignment'):
        messages.error(request, 'К этой теме нет контрольной точки')
        return redirect('topics:detail', topic_id=topic_id)
    
    assignment = topic.assignment
    
    if Submission.objects.filter(student=student, assignment=assignment).exists():
        messages.error(request, 'Вы уже отправили ответ на эту контрольную точку')
        return redirect('topics:detail', topic_id=topic_id)
    
    answer = request.POST.get('answer')
    if not answer:
        messages.error(request, 'Пожалуйста, введите ответ')
        return redirect('topics:detail', topic_id=topic_id)
    
    Submission.objects.create(
        student=student,
        assignment=assignment,
        answer=answer
    )
    
    messages.success(request, 'Ответ успешно отправлен!')
    return redirect('topics:detail', topic_id=topic_id)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Course, Topic
from assignments.models import Assignment, Submission
from students.models import Student


@login_required(login_url='/auth/login/')
def course_list(request):
    """Страница курсов с баллами и оценкой"""
    try:
        student = Student.objects.get(account=request.user)
        courses = Course.objects.filter(group=student.group).select_related('discipline', 'teacher')
        
        for course in courses:
            topics = Topic.objects.filter(discipline=course.discipline)
            
            assignments = Assignment.objects.filter(topic__in=topics)
            
            course.max_total_score = assignments.aggregate(Sum('weight'))['weight__sum'] or 0
            
            submissions = Submission.objects.filter(
                student=student,
                assignment__in=assignments,
                score__isnull=False
            )
            course.student_total_score = submissions.aggregate(Sum('score'))['score__sum'] or 0
            
            if course.max_total_score > 0:
                course.percentage = int((course.student_total_score / course.max_total_score) * 100)
            else:
                course.percentage = 0
                
    except Student.DoesNotExist:
        courses = Course.objects.none()
        messages.warning(request, 'Ваш аккаунт не привязан к студенту')
    
    return render(request, 'courses/course_list.html', {'courses': courses})


@login_required(login_url='/auth/login/')
def course_detail(request, id):
    """Страница курса с топиками и контрольными точками"""
    course = get_object_or_404(Course, id=id)
    
    try:
        student = Student.objects.get(account=request.user)
        if course.group != student.group:
            messages.error(request, 'У вас нет доступа к этому курсу')
            return redirect('course_list')
    except Student.DoesNotExist:
        messages.error(request, 'Студент не найден')
        return redirect('course_list')
    
    topics = Topic.objects.filter(
        discipline=course.discipline
    ).order_by('ordering_number')
    
    for topic in topics:
        try:
            assignment = Assignment.objects.get(topic=topic)
            topic.has_assignment = True
            topic.max_score = assignment.weight
            
            submission = Submission.objects.filter(
                student=student,
                assignment=assignment
            ).first()
            
            if submission:
                topic.student_score = submission.score
                topic.submission_status = 'checked' if submission.score is not None else 'pending'
            else:
                topic.student_score = None
                topic.submission_status = 'not_submitted'
        except Assignment.DoesNotExist:
            topic.has_assignment = False
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'topics': topics
    })


@login_required(login_url='/auth/login/')
def topic_detail(request, topic_id):
    """Страница топика (с контрольной точкой или без)"""
    topic = get_object_or_404(Topic, id=topic_id)
    
    try:
        student = Student.objects.get(account=request.user)
        course = Course.objects.filter(
            discipline=topic.discipline,
            group=student.group
        ).first()
        
        if not course:
            messages.error(request, 'У вас нет доступа к этому топику')
            return redirect('course_list')
    except Student.DoesNotExist:
        messages.error(request, 'Студент не найден')
        return redirect('course_list')
    
    # Проверяем наличие контрольной точки
    try:
        assignment = Assignment.objects.get(topic=topic)
        has_assignment = True
        submission = Submission.objects.filter(
            student=student,
            assignment=assignment
        ).first()
    except Assignment.DoesNotExist:
        has_assignment = False
        submission = None
    
    # Обработка отправки ответа
    if request.method == 'POST' and has_assignment:
        answer_text = request.POST.get('answer', '').strip()
        
        if not answer_text:
            messages.error(request, 'Ответ не может быть пустым')
        elif submission:
            messages.warning(request, 'Вы уже отправили ответ на эту контрольную точку')
        else:
            Submission.objects.create(
                student=student,
                assignment=assignment,
                answer=answer_text,
                score=None
            )
            messages.success(request, 'Ответ успешно отправлен! Преподаватель проверит его в ближайшее время.')
            return redirect('topic_detail', topic_id=topic.id)
    
    return render(request, 'courses/topic_detail.html', {
        'topic': topic,
        'course': course,
        'has_assignment': has_assignment,
        'assignment': assignment if has_assignment else None,
        'submission': submission,
    })
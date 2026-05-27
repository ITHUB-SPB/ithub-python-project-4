from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Student
from content.models import Topic
from assignments.models import Assignment, Submission


def courses_list(request):
    courses = Course.objects.select_related('discipline', 'group').all()

    # Получаем текущего студента
    student = None
    if request.user.is_authenticated:
        try:
            student = request.user.student_profile
        except:
            pass

    # Собираем данные о баллах для каждого курса
    courses_data = []
    for course in courses:
        total_score = 0
        total_weight = 0
        if student:
            assignments = Assignment.objects.filter(topic__discipline=course.discipline)
            for assignment in assignments:
                total_weight += assignment.weight
                try:
                    submission = Submission.objects.get(student=student, assignment=assignment)
                    if submission.score:
                        total_score += submission.score
                except Submission.DoesNotExist:
                    pass

        # Вычисляем оценку (примерная логика)
        grade = None
        if total_weight > 0:
            percentage = (total_score / total_weight) * 100
            if percentage >= 86:
                grade = 5
            elif percentage >= 70:
                grade = 4
            elif percentage >= 56:
                grade = 3
            else:
                grade = 2

        courses_data.append({
            'course': course,
            'total_score': total_score,
            'total_weight': total_weight,
            'grade': grade,
        })

    return render(request, 'courses/list.html', {'courses_data': courses_data})


def course_detail(request, course_id):
    course = get_object_or_404(
        Course.objects.select_related('discipline', 'group', 'teacher'),
        id=course_id
    )

    # Получаем топики для дисциплины курса
    topics = Topic.objects.filter(discipline=course.discipline).order_by('ordering_number')

    # Получаем текущего студента
    student = None
    if request.user.is_authenticated:
        try:
            student = request.user.student_profile
        except:
            pass

    # Собираем данные о баллах для каждого топика
    topics_data = []
    for topic in topics:
        has_assignment = False
        assignment = None
        submission = None
        score_display = None

        try:
            assignment = Assignment.objects.get(topic=topic)
            has_assignment = True
            if student:
                try:
                    submission = Submission.objects.get(student=student, assignment=assignment)
                    if submission.score:
                        score_display = f"{submission.score}/{assignment.weight}"
                    else:
                        score_display = "На проверке"
                except Submission.DoesNotExist:
                    score_display = f"0/{assignment.weight}"
        except Assignment.DoesNotExist:
            pass

        topics_data.append({
            'topic': topic,
            'has_assignment': has_assignment,
            'score_display': score_display,
        })

    return render(request, 'courses/detail.html', {
        'course': course,
        'topics': topics_data,
    })


def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    # Проверяем, есть ли контрольная точка
    has_assignment = False
    assignment = None
    submission = None
    already_submitted = False

    try:
        assignment = Assignment.objects.get(topic=topic)
        has_assignment = True
    except Assignment.DoesNotExist:
        pass

    # Получаем текущего студента
    student = None
    if request.user.is_authenticated:
        try:
            student = request.user.student_profile
            if has_assignment:
                try:
                    submission = Submission.objects.get(student=student, assignment=assignment)
                    already_submitted = True
                except Submission.DoesNotExist:
                    pass
        except:
            pass

    # Обработка отправки ответа
    if request.method == 'POST' and has_assignment and not already_submitted:
        answer = request.POST.get('answer', '').strip()
        if answer:
            Submission.objects.create(
                student=student,
                assignment=assignment,
                answer=answer,
                score=None
            )
            messages.success(request, 'Ответ успешно отправлен!')
            return HttpResponseRedirect(reverse('topic_detail', args=[topic_id]))
        else:
            messages.error(request, 'Пожалуйста, введите ответ')

    return render(request, 'courses/topic_detail.html', {
        'topic': topic,
        'has_assignment': has_assignment,
        'assignment': assignment,
        'already_submitted': already_submitted,
        'submission': submission,
    })
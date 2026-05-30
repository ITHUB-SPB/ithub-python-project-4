from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from courses import models


@login_required(login_url=reverse_lazy('login'))
def index(request):
	group = request.user.student.group
	courses = models.Course.objects.filter(group=group)

	return render(
		request,
		'courses.html',
		{ 'courses': courses }
	)


@login_required(login_url=reverse_lazy('login'))
def detail(request, course_id):
	course = models.Course.objects.get(pk=course_id)

	return render(
		request,
		'course_detail.html',
		{ 'course': course }
	)


@login_required(login_url=reverse_lazy('login'))
def topic(request, course_id, topic_id):
	topic = models.Topic.objects.get(pk=topic_id)

	submission = models.Submission.objects.filter(
		assignment=topic.assignment,
		student=request.user.student
	).first()

	if request.method == 'POST':
		models.Submission(
			student=request.user.student,
			answer=request.POST.get('answer'),
			assignment=topic.assignment
		).save()

		messages.success(request, message='Ответ отправлен!')
		return redirect(
			reverse(
				'topic',
				kwargs={ "course_id": course_id, "topic_id": topic_id }
			)
		)


	return render(
		request,
		'topic.html',
		{ 'topic': topic, 'submission': submission }
	)
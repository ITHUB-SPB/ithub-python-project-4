from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render
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
from django.shortcuts import render
from courses import models


def index(request):
	disciplines = models.Discipline.objects.all()

	return render(
		request,
		'courses.html',
		{ 'disciplines': disciplines }
	)


def detail(request, course_id):
	discipline = models.Discipline.objects.get(pk=course_id)

	return render(
		request,
		'course_detail.html',
		{ 'discipline': discipline }
	)
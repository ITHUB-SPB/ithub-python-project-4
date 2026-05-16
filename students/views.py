from django.contrib import auth, messages
from django.shortcuts import render, redirect, reverse


def login(request):
	if request.method == 'GET':
		return render(request, 'login.html')

	username = request.POST.get('username')
	password = request.POST.get('password')

	user = auth.authenticate(
		request,
		username=username,
		password=password
	)

	if not user:
		messages.error(request, message='Не удалось войти')
		return redirect(reverse('login'))

	auth.login(request, user)
	return redirect(reverse('index'))


def logout(request):
	auth.logout(request)
	return redirect(reverse('login'))
from django.contrib import messages, auth
from django.shortcuts import render, redirect, reverse


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = auth.authenticate(request, username=username, password=password)

    if not user:
        messages.error(request, message='Пользователь не найден')
        return redirect(reverse('login'))

    auth.login(request, user)

    messages.success(request, message='С возвращением!')

    return redirect(reverse('courses_list'))
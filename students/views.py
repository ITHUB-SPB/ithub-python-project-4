from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from django.urls import reverse


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is None:
        messages.error(request, 'Неверный логин или пароль')
        return redirect(reverse('login'))

    auth_login(request, user)
    return redirect(reverse('courses'))


def logout(request):
    auth_logout(request)
    return redirect(reverse('login'))
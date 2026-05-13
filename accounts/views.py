from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth import forms


def login(request):
    form = forms.AuthenticationForm(request.POST or None)

    if request.method == 'GET':
        return render(
            request,
            'accounts/login.html',
            {"form": form}
        )

    username = request.POST.get('username')
    password = request.POST.get('password')

    if user := auth.authenticate(request, username=username, password=password):
        auth.login(request, user)
        return redirect(reverse('courses'))

    messages.error(request, 'Не удалось войти. Попробуйте снова')

    return render(
            request,
            'accounts/login.html',
            {"form": form}
        )

def signup(request):
    form = forms.UserCreationForm(request.POST or None)

    if request.method == 'GET':
        return render(
            request,
            'accounts/signup.html',
            {"form": form}
        )

    if not form.is_valid():
        messages.error(request, "Не удалось создать аккаунт")
        return render(
            request,
            'accounts/signup.html',
            {"form": form}
        )

    username = form.cleaned_data['username']
    password = form.cleaned_data['password1']

    User = auth.get_user_model()
    User.objects.create_user(
        username=username,
        password=password,
    )

    return redirect(reverse('login'))


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))

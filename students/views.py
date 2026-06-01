from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.urls import reverse

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(request, username=username, password=password)

    if not user:
        messages.error(request, 'Не удалось войти')
        return redirect(reverse('login'))
        
    auth.login(request, user)
    print(user.is_staff)
    if user.is_staff:
        return redirect(reverse('staff'))
    else:
        return redirect(reverse('courses'))


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from accounts.forms import LoginForm


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        if getattr(request.user, "profile", None) is not None and hasattr(request.user, "student"):
            return redirect("courses:list")
        return redirect("/admin/")
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            fallback_url = "courses:list" if hasattr(user, "student") else "/admin/"
            return redirect(request.GET.get("next") or request.POST.get("next") or fallback_url)
        messages.error(request, "Неверный логин или пароль.")
    return render(request, "accounts/login.html", {"form": form, "next": request.GET.get("next", "")})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("accounts:login")

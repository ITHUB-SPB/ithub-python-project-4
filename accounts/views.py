from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from accounts.forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("/admin/")
        return redirect("courses:list")
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        next_url = request.POST.get("next") or request.GET.get("next")
        if next_url:
            return redirect(next_url)
        if request.user.is_staff:
            return redirect("/admin/")
        return redirect("courses:list")
    if request.method == "POST":
        for error in form.non_field_errors():
            messages.error(request, error)
    return render(request, "accounts/login.html", {"form": form, "next": request.GET.get("next", "")})


def logout_view(request):
    logout(request)
    return redirect("accounts:login")

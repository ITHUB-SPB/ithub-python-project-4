from django import forms
from django.contrib.auth import authenticate
from unfold import forms as unfold_forms


class AdminPasswordChangeForm(unfold_forms.AdminPasswordChangeForm):
    pass


class UserChangeForm(unfold_forms.UserChangeForm):
    pass


class UserCreationForm(unfold_forms.UserCreationForm):
    pass


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Логин")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            self.user = authenticate(self.request, username=username, password=password)
            if self.user is None:
                raise forms.ValidationError("Неверный логин или пароль")
        return cleaned_data

    def get_user(self):
        return self.user

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminPasswordChangeForm as DjangoAdminPasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField


User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", strip=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "is_staff", "is_superuser")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            self.save_m2m()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Пароль")

    class Meta:
        model = User
        fields = ("username", "password", "is_staff", "is_superuser", "groups", "user_permissions")

    def clean_password(self):
        return self.initial["password"]


class AdminPasswordChangeForm(DjangoAdminPasswordChangeForm):
    pass

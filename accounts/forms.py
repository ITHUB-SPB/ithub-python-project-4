from unfold import forms as unfold_forms
from accounts import models

class AdminPasswordChangeForm(unfold_forms.AdminPasswordChangeForm):
    pass


class UserChangeForm(unfold_forms.UserChangeForm):
    class Meta:
        model = models.User
        fields = ['username', 'is_staff', 'is_superuser', 'groups']


class UserCreationForm(unfold_forms.UserCreationForm):
    pass

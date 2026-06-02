from django import forms

from courses.models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ("message", "attachment")
        widgets = {
            "message": forms.Textarea(attrs={"rows": 6, "placeholder": "Сообщение..."}),
        }

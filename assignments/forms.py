from django import forms

class SubmissionForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea, label='Ваш ответ')
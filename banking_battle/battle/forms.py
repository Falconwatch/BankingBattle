from django import forms
from .models import Submit, Team

class SubmitForm(forms.ModelForm):
    class Meta:
        model = Submit
        fields = ['file', 'team', 'round']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name"]
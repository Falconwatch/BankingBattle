from django import forms
from .models import Submit

class SubmitForm(forms.ModelForm):
    class Meta:
        model = Submit
        fields = ['file', 'team', 'round']
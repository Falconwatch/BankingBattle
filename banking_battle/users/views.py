from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


# Регистрация (signup/)
class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('battle:index')
    template_name = 'users/signup.html'

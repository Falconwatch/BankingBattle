from django.shortcuts import get_object_or_404, redirect, render

from .models import User

def index(request):    
    template = 'battle/index.html'
    return render(request, template) 

def profile(request, username):
    template = 'battle/profile.html'
    author = get_object_or_404(User, username=username)
    context = {
        'author': author,
    }
    return render(request, template, context)
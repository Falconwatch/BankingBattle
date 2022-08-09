from django.contrib.auth.decorators import login_required
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


@login_required
def results(request):
    template = 'battle/game_results.html'
    return render(request, template) 

@login_required
def leaders(request):
    template = 'battle/game_leaders.html'
    return render(request, template) 

@login_required
def game_main(request):
    template = 'battle/game.html'
    return render(request, template) 
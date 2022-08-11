import mimetypes
import os

from banking_battle.settings import BASE_DIR
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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

@login_required
def download_file(request):
    # fill these variables with real values
    fl_path = os.path.join(BASE_DIR, 'data/test.txt') 
    filename = 'test.txt'

    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

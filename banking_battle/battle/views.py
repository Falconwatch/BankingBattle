import mimetypes
import os

from banking_battle.settings import BASE_DIR
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import User, Game


def index(request):
    user = request.user
    if user:
        template = 'battle/index_signedin.html'
        users_teams = user.users_teams.all()
        context = {
            'user': user,
            'users_teams': users_teams
        }
        return render(request, template, context)
    else:
        template = 'battle/index.html'
        return render(request, template)


def profile(request, username):
    template = 'battle/profile.html'
    user = get_object_or_404(User, username=username)
    users_teams = user.users_teams.all()
    context = {
        'user': user,
        'users_teams': users_teams
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
def game(request, gameid):
    user = request.user
    game = Game.objects.get(pk=gameid)
    #ToDo: упростить блок ниже
    user_in_team = False
    for team in user.users_teams.all():
        if team.game.id == gameid:
            user_in_team = True

    template = 'battle/game.html'
    context = {"game": game, "show_submit_form": user_in_team} # Если пользователь участвует в соревновании, доступна форма сабмита
    return render(request, template, context)


def games(request):
    template = 'battle/games.html'
    all_games = Game.objects.all()
    context = {"all_games": all_games}
    return render(request, template, context)

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

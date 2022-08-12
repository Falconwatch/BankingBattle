import mimetypes
import os
from banking_battle.settings import BASE_DIR
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from .models import User, Game, Round, Submit, Team
from .forms import SubmitForm


def index(request):
    user = request.user
    if user.is_anonymous:
        template = 'battle/index.html'
        return render(request, template)
    else:
        template = 'battle/index_signedin.html'
        users_teams = user.users_teams.all()
        context = {
            'user': user,
            'users_teams': users_teams
        }
        return render(request, template, context)


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
    # ToDo: упростить блок ниже
    user_in_team = False
    for team in user.users_teams.all():
        if team.game.id == gameid:
            print("here")
            print(team.game.id, gameid)
            user_in_team = True
    print(user_in_team)
    game_rounds = game.rounds.all()

    template = 'battle/game.html'
    context = {"game": game,
               "show_submit_form": user_in_team,
               "game_rounds": game_rounds}  # Если пользователь участвует в соревновании, доступна форма сабмита
    return render(request, template, context)


def games(request):
    template = 'battle/games.html'
    all_games = Game.objects.all()
    context = {"all_games": all_games}
    return render(request, template, context)


@login_required
def round(request, roundid):
    template = 'battle/round.html'
    game_round = Round.objects.get(pk=roundid)
    game = game_round.game
    user = request.user
    team = Team.objects.filter(users_in_team__id__contains = user.id).first()
    team_submits_in_this_round = Submit.objects.filter(round__id=roundid).filter(team__id = team.id).all()

    if request.method == 'POST' and len(request.FILES)>0:
        upload = request.FILES['upload']
        fss = FileSystemStorage(location="submits/")
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        submit = Submit(team = team,
                    round = game_round,
                      file = file)
        submit.save()
        context = {"game": game,
                   "round": game_round,
                   'file_url': file_url,
                   "team_submits": team_submits_in_this_round}
        return render(request, template, context)
    else:
        context = {"game": game,
                   "round": game_round,
                   "team_submits": team_submits_in_this_round}
        return render(request, template, context)

@login_required
def download_submit(request, submit_id):
    user = request.user
    team = Team.objects.filter(users_in_team__id__contains = user.id).first()
    submit = Submit.objects.filter(id=submit_id).filter(team__id = team.id).first()

    file_name = submit.file.name

    # get the download path
    download_path = os.path.join("submits/", file_name)

    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_name)
            return response
    raise Http404



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



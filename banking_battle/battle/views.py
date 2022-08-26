import mimetypes
import os
from collections import defaultdict

import django.db.models as f
from banking_battle.settings import BASE_DIR
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render

from .models import User, Game, Round, Submit, Team


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
    team = Team.objects.filter(game__id=1).filter(users_in_team__in=[user.id]).first()

    # тут собираем лидерборд
    submits_in_game = Submit.objects.filter(round__game__id=gameid)
    teams_results_in_rounds = (
        submits_in_game.values("team__name", "team__id", "round").annotate(round_result=f.Max("result")).all())

    teams_results_in_game_dict = defaultdict(lambda: 0)
    for team_result_in_round in teams_results_in_rounds:
        team_identifier = (team_result_in_round["team__id"], team_result_in_round["team__name"])
        teams_results_in_game_dict[team_identifier] += team_result_in_round["round_result"]

    teams_results_in_game = [(idenifier, result, 0) for idenifier, result in
                             teams_results_in_game_dict.items()]
    teams_results_in_game = sorted(teams_results_in_game, key=lambda x: x[1], reverse=True)


    # Тут определяем, состоит ли пользователь в команде, участвующей в игре и результат его команды
    user_in_team = True if team else False
    user_result = dict()
    if user_in_team:
        user_result = {"result": teams_results_in_game_dict[(team.id, team.name)],
                       "team_name": team.name}
        teams_results_in_game = [(idenifier, result, 1 if idenifier[0] == team.id else 0) for idenifier, result, flag in
                                 teams_results_in_game]

    # Выводим список раундов
    game_rounds = game.rounds.all()

    template = 'battle/game.html'
    context = {"game": game,
               "leader_board": teams_results_in_game,
               "user_in_team": user_in_team,
               "user_result": user_result,
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
    team = Team.objects.filter(users_in_team__id__contains=user.id).first()
    team_submits_in_this_round = Submit.objects.filter(round__id=roundid).filter(team__id=team.id).all()

    if request.method == 'POST' and len(request.FILES) > 0:
        upload = request.FILES['upload']
        fss = FileSystemStorage(location="submits/")
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        submit = Submit(team=team,
                        round=game_round,
                        file=file)
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
    team = Team.objects.filter(users_in_team__id__contains=user.id).first()
    submit = Submit.objects.filter(id=submit_id).filter(team__id=team.id).first()

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


@login_required
def team_create(request):
    template = 'battle/team_create.html'
    context = {}
    #TODO: передавать с какой игры был выполнене переход, если не с какой - кидай 404
    if request.method == 'POST':
        pass
    else:
        current_user = request.user
        current_user_team = Team.objects.filter(users_in_team__id = current_user.id).first()
        if current_user_team:
            context["team_name"] = current_user_team.name
            u_in_team = current_user_team.users_in_team.values('id', 'username').all()
            context["user_has_team"] = True
            context["user_in_team"] = u_in_team

    return render(request, template, context)

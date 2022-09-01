import mimetypes
import os
from collections import defaultdict

import django.db.models as f
from banking_battle.settings import BASE_DIR
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render

from .forms import ApplicationForm
from .managers import *

from .models import User, Game, Round, Submit, Team, TeamInvitation


def index(request):
    user = request.user
    if user.is_anonymous:
        template = 'battle/index.html'
        return render(request, template)
    else:
        template = 'battle/index_signedin.html'
        users_teams = get_teams(user_id=user.id)
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
    team = get_teams(user_id=user.id, game_id=game.id)

    #team = Team.objects.filter(game__id=1).filter(users_in_team__in=[user.id]).first()

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
                       "team_name": team.name,}
        teams_results_in_game = [(idenifier, result, 1 if idenifier[0] == team.id else 0) for idenifier, result, flag in
                                 teams_results_in_game]

    # Выводим список раундов
    game_rounds = game.rounds.all()

    template = 'battle/game.html'
    context = {"game": game,
               "team":team,
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
    team = get_teams(user_id=user.id, game_id=game.id)
    #team = Team.objects.filter(users_in_team__id__contains=user.id).first()
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
    teams = get_teams(user_id=user.id)
    #team = Team.objects.filter(users_in_team__id__contains=user.id).first()
    submit = Submit.objects.filter(id=submit_id).filter(team = teams).first()

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
def apply(request, gameid):
    def get_unique_rand():
        while True:
            code = User.objects.make_random_password()
            if not Team.objects.filter(invite_code = code).exists():
                return code
    template = 'battle/apply.html'
    context = {}
    #проверяем есть ли такая игра, если нет - 404
    game = get_object_or_404(Game, id=gameid)
    context["game_title"] = game.title
    context["game_id"] = game.id
    current_user = request.user
    #теперь ветвление по логике
    if request.method == 'POST': #если пришёл POST запрос, это сабмит формы-заявки
        application_form = ApplicationForm(request.POST)
        if application_form.is_valid():
            team_application = Team(state = "application", game = game)
            team_application.creator = current_user
            team_application.name = application_form.cleaned_data['name']
            team_application.invite_code = get_unique_rand()
            team_application.save()
            team_application.users_in_team.set([current_user])
            team_application.save()
            context["state"] = "applied"
            render(request, template, context)
    else: #в ином случае проверяем нет ли активнйо заявки: есть - показываем её, нет - выводим форму
        application = get_created_application(creator_id=current_user.id, game_id=game.id)
        if application:
            context["state"] = "application"
            context["team_name"] = application.name
        else: #заявок нет - ищем команду
            team = get_created_teams(creator_id=current_user.id, game_id=game.id)
            if team:
                context["state"] = "active_team"
                context["team_name"] = team.name
            else: #нет ни заявки, ни команды - показываем форму
                context["state"] = "none"
    return render(request, template, context)


@login_required
def manage_team(request, teamid):
    template = 'battle/team.html'

    team = get_object_or_404(Team, id=teamid)
    users = get_team_users(team=team)
    invitations = TeamInvitation.objects.filter(team = team)

    context = {}
    context["team"] = team
    context["users_in_team"] = users
    context["invitations"] = invitations
    context["invitation_code"] = team.invite_code

    return render(request,template,context)

@login_required()
def join_team(request, code):
    template = "battle/join_team.html"
    team = get_object_or_404(Team, invite_code = code)
    user = request.user
    team_invitation_exists = TeamInvitation.objects.filter(team=team).filter(user=user).exists()
    user_in_team = team.users_in_team.filter(id=user.id).exists()

    context = {}
    context['team'] = team
    context['invitation_code'] = code

    if user_in_team:
        context['state'] = "user_in_team"
        return render(request, template, context)

    if request.method=="POST": #пришла заявка на вступление
        if not team_invitation_exists:
            invitation = TeamInvitation()
            invitation.user = user
            invitation.team = team
            invitation.save()
            context['state'] = "accepted"
        else:
            context['state'] = "exists"
    else:
        if team_invitation_exists:
            context['state'] = "exists"
        else:
            context['state'] = "enable"
    return render(request, template, context)

def join_team_overview(request, joinid):
    template = "battle/join_team_overview.html"
    context={}
    team_join = get_object_or_404(TeamInvitation, id = joinid)
    joining_user = team_join.user
    joining_team = team_join.team
    print(joining_team)

    context["team"] = joining_team
    context["user"] = joining_user
    context["state"] = "first"

    if request.method=="POST":
        if request.POST.get("yes"):#принимаем пользователя в команду
            joining_team.users_in_team.add(joining_user)
            context["state"] = "Принято"
            team_join.delete()
        elif request.POST.get("no"):#отказываем и удаляем заявку
            context["state"] = "Отказано"
            team_join.delete()

    return render(request, template, context)
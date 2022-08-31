from django.urls import path
from . import views

app_name = 'battle'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('game/<int:gameid>/', views.game, name='game'),
    path('game/resuls/', views.results, name='results'),
    path('game/leaders/', views.leaders, name='leaders'),
    path('games/', views.games, name='games'),
    path('game/download', views.download_file, name='download'),
    path('round/<int:roundid>/', views.round, name='round'),
    path('download_submit/<int:submit_id>', views.download_submit, name='download_submit'),
    path('apply/<int:gameid>', views.apply, name='apply'),
    path('team/<int:teamid>', views.manage_team, name="team"),
    path('join_team/<str:code>', views.join_team, name="join_team"),
    path('join_team_overview/<int:joinid>', views.join_team_overview, name="join_team_overview")

] 
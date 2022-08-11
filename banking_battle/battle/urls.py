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
    path('round/<int:roundid>/', views.round, name='round')
] 
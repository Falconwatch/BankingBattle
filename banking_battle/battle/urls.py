from django.urls import path
from . import views

app_name = 'battle'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('game/resuls/', views.results, name='results'),
    path('game/leaders/', views.leaders, name='leaders'),
    path('game/', views.game_main, name='game_main'),
    path('game/download', views.download_file, name='download')
] 
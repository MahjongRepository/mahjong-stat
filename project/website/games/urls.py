from django.conf.urls import url
from django.urls import path

from website.games import views

urlpatterns = [
    path('players/total/', views.total_statistics, name='total_statistics'),
    path('players/<int:player_id>/', views.player_statistics, name='player_statistics'),
    path('game/<int:game_id>/', views.game_details, name='game_details'),
    path('game/load/<int:game_id>/', views.manually_load_results, name='manually_load_results'),
]

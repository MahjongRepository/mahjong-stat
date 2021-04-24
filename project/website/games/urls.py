from django.conf.urls import url
from django.urls import path

from website.games import views

urlpatterns = [
    url(r'^players/total/$', views.total_statistics, name='total_statistics'),
    path('players/<int:player_id>/', views.player_statistics, name='player_statistics'),
    url(r'^game/load/(?P<game_id>[^/]+)/$', views.manually_load_results, name='manually_load_results'),
]

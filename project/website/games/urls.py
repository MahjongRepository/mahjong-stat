from django.conf.urls import url

from website.games import views

urlpatterns = [
    url(r'^players/(?P<player_name>[^/]+)/$', views.player_statistics, name='player_statistics'),
    url(r'^game/load/(?P<game_id>[^/]+)/$', views.manually_load_results, name='manually_load_results'),
]

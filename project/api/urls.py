from django.conf.urls import url

from api import views

urlpatterns = [
    url(r'^tenhou/game/start/$', views.start_tenhou_game, name='api_start_tenhou_game'),
    url(r'^tenhou/game/finish/$', views.finish_tenhou_game, name='api_finish_tenhou_game'),
]

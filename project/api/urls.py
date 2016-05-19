from django.conf.urls import url

from api import views

urlpatterns = [
    url(r'^tenhou/game/add/$', views.add_tenhou_game, name='api_add_tenhou_game')
]

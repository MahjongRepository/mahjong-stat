from django.conf.urls import url, include

from website import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^', include('website.games.urls')),
]

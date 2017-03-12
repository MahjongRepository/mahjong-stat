from django.conf.urls import url

from website.events import views

urlpatterns = [
    url(r'^events/(?P<slug>[^/]+)/add_game/$', views.add_game, name='add_game'),
    url(r'^events/(?P<slug>[^/]+)/$', views.details, name='event_details'),
]

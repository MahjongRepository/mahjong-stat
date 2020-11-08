from django.http import HttpResponse
from django.shortcuts import render

from website.accounts.models import Player


def home(request):
    players = Player.objects.all()
    return render(request, 'home.html', {'players': players})

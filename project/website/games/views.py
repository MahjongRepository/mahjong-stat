from django.db.models import Avg
from django.shortcuts import render, get_object_or_404

from website.accounts.models import Player


def player_statistics(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    games = player.games.all()[:10  ]
    average_position = player.games.all().aggregate(Avg('player_position'))['player_position__avg']
    return render(request, 'website/player_statistics.html',
                  {'player': player, 'games': games, 'average_position': average_position})

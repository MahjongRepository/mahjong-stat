from django.db.models import Avg
from django.shortcuts import render, get_object_or_404

from website.accounts.models import Player
from website.games.models import GameRound


def player_statistics(request, player_id):
    player = get_object_or_404(Player, id=player_id)

    games = player.games.all()
    total_games = games.count()

    total_rounds = GameRound.objects.filter(game__player=player).count()
    deal_rounds = GameRound.objects.filter(game__player=player, is_deal=True).count()
    win_rounds = GameRound.objects.filter(game__player=player, is_win=True).count()
    open_hand_rounds = GameRound.objects.filter(game__player=player, is_open_hand=True).count()
    riichi_rounds = GameRound.objects.filter(game__player=player, is_riichi=True).count()

    feed_rate = (deal_rounds / total_rounds) * 100
    win_rate = (win_rounds / total_rounds) * 100
    call_rate = (open_hand_rounds / total_rounds) * 100
    riichi_rate = (riichi_rounds / total_rounds) * 100

    average_position = games.aggregate(Avg('player_position'))['player_position__avg']
    average_deal_scores = (GameRound.objects
                           .filter(game__player=player, is_deal=True)
                           .aggregate(Avg('lose_scores'))['lose_scores__avg'])
    average_win_scores = (GameRound.objects
                          .filter(game__player=player, is_win=True)
                          .aggregate(Avg('win_scores'))['win_scores__avg'])

    return render(request, 'website/player_statistics.html', {
        'player': player,
        'games': games[:20],
        'total_games': total_games,
        'average_position': average_position,
        'average_deal_scores': average_deal_scores,
        'average_win_scores': average_win_scores,
        'feed_rate': feed_rate,
        'win_rate': win_rate,
        'call_rate': call_rate,
        'riichi_rate': riichi_rate,
    })

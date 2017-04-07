from django.db.models import Avg
from django.shortcuts import render, get_object_or_404

from website.accounts.models import Player
from website.games.models import GameRound


def player_statistics(request, player_name):
    player = get_object_or_404(Player, username=player_name)

    games = player.games.all().order_by('-game_date', '-id')
    total_games = games.count()

    rounds = GameRound.objects.filter(game__player=player)
    total_rounds = rounds.count()
    deal_rounds = rounds.filter(is_deal=True).count()
    win_rounds = rounds.filter(is_win=True).count()
    open_hand_rounds = rounds.filter(is_open_hand=True).count()
    riichi_rounds = rounds.filter(is_riichi=True).count()

    feed_rate = (deal_rounds / total_rounds) * 100
    win_rate = (win_rounds / total_rounds) * 100
    call_rate = (open_hand_rounds / total_rounds) * 100
    riichi_rate = (riichi_rounds / total_rounds) * 100

    riichi_successful = rounds.filter(is_riichi=True, is_win=True).count()
    riichi_failed = riichi_rounds - riichi_successful
    riichi_successful = riichi_rounds and (riichi_successful / riichi_rounds) * 100 or 0
    riichi_failed = riichi_rounds and (riichi_failed / riichi_rounds) * 100 or 0

    win_with_riichi = rounds.filter(is_riichi=True, is_win=True).count()
    win_with_open_hand = rounds.filter(is_open_hand=True, is_win=True).count()
    win_with_damaten = rounds.filter(is_damaten=True, is_win=True).count()
    win_with_riichi = win_rounds and (win_with_riichi / win_rounds) * 100 or 0
    win_with_open_hand = win_rounds and (win_with_open_hand / win_rounds) * 100 or 0
    win_with_damaten = win_rounds and (win_with_damaten / win_rounds) * 100 or 0

    feed_when_riichi = rounds.filter(is_riichi=True, is_deal=True).count()
    other_feed = deal_rounds and ((deal_rounds - feed_when_riichi) / deal_rounds) * 100 or 0
    feed_when_riichi = deal_rounds and (feed_when_riichi / deal_rounds) * 100 or 0

    call_and_win = rounds.filter(is_open_hand=True, is_win=True).count()
    call_and_deal = rounds.filter(is_open_hand=True, is_deal=True).count()
    call_and_win = open_hand_rounds and (call_and_win / open_hand_rounds) * 100 or 0
    call_and_deal = open_hand_rounds and (call_and_deal / open_hand_rounds) * 100 or 0
    call_and_other = 100 - call_and_deal - call_and_win

    average_position = games.aggregate(Avg('player_position'))['player_position__avg']
    average_deal_scores = (rounds
                           .filter(is_deal=True)
                           .aggregate(Avg('lose_scores'))['lose_scores__avg'])
    average_win_scores = (rounds
                          .filter(is_win=True)
                          .aggregate(Avg('win_scores'))['win_scores__avg'])

    first_position_games = games.filter(player_position=1).count()
    second_position_games = games.filter(player_position=2).count()
    third_position_games = games.filter(player_position=3).count()
    fourth_position_games = games.filter(player_position=4).count()
    bankruptcy_games = games.filter(scores__lt=0).count()

    first_position_rate = (first_position_games / total_games) * 100
    second_position_rate = (second_position_games / total_games) * 100
    third_position_rate = (third_position_games / total_games) * 100
    fourth_position_rate = (fourth_position_games / total_games) * 100
    bankruptcy_rate = (bankruptcy_games / total_games) * 100

    return render(request, 'website/player_statistics.html', {
        'player': player,
        'games': games[:40],
        'total_games': total_games,

        'average_position': average_position,
        'average_deal_scores': average_deal_scores,
        'average_win_scores': average_win_scores,

        'feed_rate': feed_rate,
        'win_rate': win_rate,
        'call_rate': call_rate,
        'riichi_rate': riichi_rate,

        'riichi_successful': riichi_successful,
        'riichi_failed': riichi_failed,

        'first_position_rate': first_position_rate,
        'second_position_rate': second_position_rate,
        'third_position_rate': third_position_rate,
        'fourth_position_rate': fourth_position_rate,
        'bankruptcy_rate': bankruptcy_rate,

        'win_with_riichi': win_with_riichi,
        'win_with_open_hand': win_with_open_hand,
        'win_with_damaten': win_with_damaten,

        'feed_when_riichi': feed_when_riichi,
        'other_feed': other_feed,

        'call_and_win': call_and_win,
        'call_and_deal': call_and_deal,
        'call_and_other': call_and_other,
    })
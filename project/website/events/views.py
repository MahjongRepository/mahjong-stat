import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from tenhou_log_parser.main import TenhouLogParser
from website.accounts.models import Player
from website.events.models import MahjongEvent, EventPlayer, EventGame
from website.games.models import Game, GameRound


def details(request, slug):
    event = get_object_or_404(MahjongEvent, slug=slug)
    players = EventPlayer.objects.filter(event=event).order_by('-rate')
    games = EventGame.objects.filter(event=event).order_by('-game_date')
    return render(request, 'events/details.html', {'event': event, 'players': players, 'games': games})


@login_required
def add_game(request, slug):
    event = get_object_or_404(MahjongEvent, slug=slug)

    # EventGame.objects.all().delete()
    # Game.objects.all().delete()
    # GameRound.objects.all().delete()
    # EventPlayer.objects.all().update(sum_of_places=0, played_games=0, average_place=0, rate=0)

    log_id = request.GET.get('log_id')
    results = TenhouLogParser().parse_log(log_id)
    uma = [15, 5, -5, -15]

    event_game = {'log_id': log_id, 'players': [], 'date': None}

    for player_data in results['players']:
        player = Player.objects.get(username=player_data['name'])
        event_player = EventPlayer.objects.get(player=player, event=event)

        scores = player_data['scores']
        position = player_data['position']
        rate = ((scores - 30000) / 1000) + uma[position - 1]

        event_game['players'].append({'player': player_data['name'], 'rate': rate})
        event_game['date'] = results['game_date']

        event_player.sum_of_places += position
        event_player.played_games += 1
        event_player.average_place = event_player.sum_of_places / event_player.played_games
        event_player.rate = float(event_player.rate) + rate
        event_player.save()

        game = Game.objects.create(
            player=player,
            external_id=log_id,
            player_position=player_data['position'],
            scores=player_data['scores'],
            seat=player_data['seat'],
            rate=player_data['rate'],
            rank=player_data['rank'],
            game_place=Game.TENHOU,
            game_rule=results['game_rule'],
            game_type=results['game_type'],
            game_date=results['game_date'],
            lobby=results['lobby'],
            game_log_content=results['log_data']
        )

        for round_data in player_data['rounds']:
            GameRound.objects.create(
                game=game,
                is_win=round_data['is_win'],
                is_deal=round_data['is_deal'],
                is_retake=round_data['is_retake'],
                is_tsumo=round_data['is_tsumo'],
                is_riichi=round_data['is_riichi'],
                is_open_hand=round_data['is_open_hand'],
                is_damaten=round_data['is_damaten'],
                round_number=round_data['round_number'],
                honba=round_data['honba'],
                win_scores=round_data['win_scores'],
                lose_scores=round_data['lose_scores'],
            )

    EventGame.objects.create(event=event,
                             game_date=event_game['date'],
                             external_id=event_game['log_id'],
                             result=json.dumps(event_game['players']))

    return HttpResponse('Ok')

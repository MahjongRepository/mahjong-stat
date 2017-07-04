from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.decorators import token_authentication
from tenhou_log_parser.main import TenhouLogParser
from website.games.models import Game, GameRound


@token_authentication
@csrf_exempt
def add_tenhou_game(request):
    log_id = request.POST.get('id')
    username = request.POST.get('username')

    if not log_id or not username:
        return JsonResponse({'success': False})

    player = request.user.players.filter(username=username).first()
    if not player:
        return JsonResponse({'success': False})

    if Game.objects.filter(external_id=log_id, game_place=Game.TENHOU, player__username=username).exists():
        return JsonResponse({'success': False})

    results = TenhouLogParser().parse_log(log_id)

    player_data = next((i for i in results['players'] if i['name'] == username), None)
    if not player_data:
        return JsonResponse({'success': False})

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

    return JsonResponse({'success': True})

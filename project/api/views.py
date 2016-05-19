import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.decorators import token_authentication
from tenhou_log_parser.main import TenhouLogParser
from website.games.models import Game


@token_authentication
@csrf_exempt
def add_tenhou_game(request):
    log_id = request.POST.get('id')
    players = request.user.players.all()
    usernames = players.values_list('username', flat=True)

    if not log_id or not usernames:
        return JsonResponse({'success': False})

    results = TenhouLogParser().parse_log(log_id)

    player = next((i for i in results if i['name'] in usernames), None)
    if not player:
        return JsonResponse({'success': False})

    Game.objects.create(
        player=players.get(username=player['name']),
        type=Game.TENHOU,
        external_id=log_id,
        player_position=player['position'],
        scores=player['scores'],
        seat=player['seat'],
        game_rule=Game.HANCHAN_ARI_ARI,
    )

    return JsonResponse({'success': True})

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.decorators import token_authentication
from website.games.models import Game


@token_authentication
@csrf_exempt
def add_tenhou_game(request):
    data = json.loads(request.POST.get('data'))

    player = request.user.players.all().first()

    game_rule_string = data['rule']
    game_rule = Game.TONPUSEN_ARI_ARI
    # 0,1 - tonpu-sen, ari, ari
    # 0,9 - hanchan, ari, ari
    if game_rule_string == '0,9':
        game_rule = Game.HANCHAN_ARI_ARI

    Game.objects.create(
        player=player,
        type=Game.TENHOU,
        external_id=data['id'],
        player_position=data['position'],
        scores=data['scores'],
        seat=data['seat'],
        game_rule=game_rule,
    )

    return JsonResponse({'success': True})

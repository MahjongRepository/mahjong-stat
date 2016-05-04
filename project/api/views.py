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

    Game.objects.create(
        player=player,
        type=Game.TENHOU,
        external_id=data['id'],
        player_position=data['position'],
        scores=data['scores']
    )

    return JsonResponse({'success': True})

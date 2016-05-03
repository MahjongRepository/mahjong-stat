import json

from django.http import JsonResponse

from api.decorators import token_authentication
from website.games.models import Game


@token_authentication
def add_tenhou_game(request):
    data = json.loads(request.POST.get('data'))

    Game.objects.create(
        user=request.user,
        type=Game.TENHOU,
        external_id=data['id'],
        player_position=data['position']
    )

    return JsonResponse({'success': True})

from django.conf import settings
from django.db.models import Avg
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.decorators import token_authentication
from api.utils import send_telegram_finished_game_message, send_telegram_new_rank_message
from parsers.tenhou.main import TenhouLogParser
from website.games.models import Game, GameRound


@token_authentication
@csrf_exempt
def start_tenhou_game(request):
    log_id = request.POST.get("id")
    username = request.POST.get("username")

    if not log_id or not username:
        return JsonResponse({"success": False})

    player = request.user.players.filter(username=username).first()
    if not player:
        return JsonResponse({"success": False})

    Game.objects.create(player=player, external_id=log_id, status=Game.STARTED)

    return JsonResponse({"success": True})


@token_authentication
@csrf_exempt
def finish_tenhou_game(request):
    log_id = request.POST.get("id")
    username = request.POST.get("username")

    if not log_id or not username:
        return JsonResponse({"success": False, "reason": 1})

    player = request.user.players.filter(username=username).first()
    if not player:
        return JsonResponse({"success": False, "reason": 2})

    try:
        game = Game.objects.get(player=player, external_id=log_id)
    except Game.DoesNotExist:
        return JsonResponse({"success": False, "reason": 3})

    json_response, _ = _load_log_and_update_game(game)
    return json_response


def _load_log_and_update_game(game, sent_new_rank_message=True):
    results = TenhouLogParser().parse_log(game.external_id, game.game_log_content)

    player_data = next((i for i in results["players"] if i["name"] == game.player.username), None)
    if not player_data:
        return JsonResponse({"success": False, "reason": 4}), None

    previous_game = (
        Game.objects.filter(player=game.player).filter(status=Game.FINISHED).exclude(id=game.id).first()
    )

    game.status = Game.FINISHED
    game.player_position = player_data["position"]
    game.scores = player_data["scores"]
    game.seat = player_data["seat"]
    game.rate = player_data["rate"]
    game.rank = player_data["rank"]
    game.game_rule = results["game_rule"]
    game.game_type = results["game_type"]
    game.game_date = results["game_date"]
    game.lobby = results["lobby"]
    game.game_room = results["game_room"]
    game.game_log_content = results["log_data"]

    game.save()

    if previous_game and game.rank != previous_game.rank and sent_new_rank_message:
        send_telegram_new_rank_message(
            previous_game.get_rank_display(),
            game.get_rank_display(),
            game.rate,
            Game.objects.filter(status=Game.FINISHED, player=game.player).count(),
            Game.objects.filter(status=Game.FINISHED, player=game.player)
            .all()
            .aggregate(Avg("player_position"))["player_position__avg"],
        )

    rounds = []
    for i, round_data in enumerate(player_data["rounds"]):
        rounds.append(
            GameRound(
                game=game,
                is_win=round_data["is_win"],
                is_deal=round_data["is_deal"],
                is_retake=round_data["is_retake"],
                is_tsumo=round_data["is_tsumo"],
                is_riichi=round_data["is_riichi"],
                is_open_hand=round_data["is_open_hand"],
                is_damaten=round_data["is_damaten"],
                round_number=round_data["round_number"],
                honba=round_data["honba"],
                win_scores=round_data["win_scores"],
                lose_scores=round_data["lose_scores"],
                han=round_data.get("han", 0),
                fu=round_data.get("fu", 0),
                round_counter=i,
            )
        )

    GameRound.objects.bulk_create(rounds)

    if settings.TELEGRAM_TOKEN:
        try:
            send_telegram_finished_game_message(game, rounds)
        except Exception as e:
            print(e)

    return JsonResponse({"success": True}), player_data

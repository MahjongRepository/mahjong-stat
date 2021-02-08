from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import ParseMode
from telegram.ext import Defaults, Updater
from telegram.utils.helpers import escape_markdown

from api.decorators import token_authentication
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


def _load_log_and_update_game(game):
    results = TenhouLogParser().parse_log(game.external_id, game.game_log_content)

    player_data = next((i for i in results["players"] if i["name"] == game.player.username), None)
    if not player_data:
        return JsonResponse({"success": False, "reason": 4}), None

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

    rounds = []
    best_hand_fu = 0
    for i, round_data in enumerate(player_data["rounds"]):
        if round_data["is_win"] and round_data.get("han", 0) > best_hand_fu:
            best_hand_fu = round_data.get("han")

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
            send_telegram_message(game, best_hand_fu)
        except:
            pass

    return JsonResponse({"success": True}), player_data


def send_telegram_message(game, best_hand_fu):
    message = f"Новая игра. \n\n"
    message += f"Бот занял `{game.player_position}` место (`{intcomma(game.scores)}` очков). \n\n"
    if best_hand_fu > 0:
        message += f"Лучшая рука: `{best_hand_fu}` хан. \n\n"
    message += f"Лог: {game.get_tenhou_url()}"

    defaults = Defaults(parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)
    updater = Updater(token=settings.TELEGRAM_TOKEN, use_context=True, defaults=defaults)

    message = escape_tg_message(message)
    updater.bot.send_message(chat_id=f"@{settings.TELEGRAM_CHANNEL_NAME}", text=message)


def escape_tg_message(message):
    message = escape_markdown(message, version=2)
    message = message.replace("\`", "`")
    return message

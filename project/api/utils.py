import random
import string
from typing import List

from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from telegram import ParseMode
from telegram.ext import Defaults, Updater
from telegram.utils.helpers import escape_markdown

from website.games.models import GameRound


def make_random_letters_string(length=15):
    random_chars = string.ascii_lowercase
    return "".join(random.choice(random_chars) for _ in range(length))


def make_random_letters_and_digit_string(length=15):
    random_chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(random_chars) for _ in range(length))


def send_telegram_new_rank_message(previous_rank, new_rank, new_rate, games_count):
    message = (
        f"🎉🎉🎉 Новый ранг `{previous_rank}` -> `{new_rank}` `R{int(new_rate)}`. Игр сыгранно: `{games_count}`"
    )
    send_telegram_message(message)


def send_telegram_finished_game_message(game, rounds: List[GameRound]):
    message = ""
    if game.scores < 0:
        message += "🙀 "
    elif game.scores > 50000:
        message += "😎 "

    message += f"Бот занял `{game.player_position}` место и набрал `{intcomma(game.scores)}` очков. \n\n"

    best_hand_han = 0
    best_hand_description = ""
    round_description = ""
    for round_item in rounds:
        if round_item.is_win and round_item.han > best_hand_han:
            best_hand_han = round_item.han
            best_hand_description = f"`{round_item.han}` хан и `{round_item.fu}` фу"

        if round_item.is_win:
            win_description = round_item.is_tsumo and "цумо" or "рону"
            round_description += f"{get_round_link(round_item)} Собрал руку `{round_item.han}` хан и `{round_item.fu}` фу по {win_description}"
            if round_item.is_damaten:
                round_description += " [даматен].\n"
            else:
                round_description += ".\n"
        elif round_item.is_deal:
            round_description += f"{get_round_link(round_item)} Накинул в `{round_item.han}` хан и `{round_item.fu}` фу. \n"
        elif round_item.han > 7:
            round_description += f"{get_round_link(round_item)} Противник собрал жирную руку в `{round_item.han}` хан и `{round_item.fu}` фу. \n"

    if best_hand_description:
        message += f"Лучшая собранная рука: {best_hand_description}. \n\n"

    message += "Краткое описание происходящего: \n"
    if round_description:
        message += round_description
        message += "\n"
    else:
        message += "Никуда не накинул и ничего не собрал. Чиллил всю игру. \n\n"

    message += f"Лог: {game.get_tenhou_url()}"

    send_telegram_message(message)


def send_telegram_message(message):
    defaults = Defaults(parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)
    updater = Updater(token=settings.TELEGRAM_TOKEN, use_context=True, defaults=defaults)

    message = escape_tg_message(message)
    updater.bot.send_message(chat_id=f"@{settings.TELEGRAM_CHANNEL_NAME}", text=message)


def escape_tg_message(message):
    message = escape_markdown(message, version=2)
    message = message.replace("\`", "`")
    message = message.replace("\[", "[")
    message = message.replace("\]", "]")
    message = message.replace("\(", "(")
    message = message.replace("\)", ")")
    return message


def get_round_link(round_item):
    return f"[{round_item.round_number_display()}]({round_item.get_tenhou_url_for_round()})"

import random
import string

from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from telegram import ParseMode
from telegram.ext import Defaults, Updater
from telegram.utils.helpers import escape_markdown


def make_random_letters_string(length=15):
    random_chars = string.ascii_lowercase
    return ''.join(random.choice(random_chars) for _ in range(length))


def make_random_letters_and_digit_string(length=15):
    random_chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(random_chars) for _ in range(length))


def send_telegram_new_rank_message(previous_rank, new_rank, new_rate):
    message = f"Новый ранг `{previous_rank}` -> `{new_rank}` (`R{int(new_rate)}`)"
    send_telegram_message(message)


def send_telegram_finished_game_message(game, best_hand_fu):
    message = f"Новая игра. \n\n"
    message += f"Бот занял `{game.player_position}` место (`{intcomma(game.scores)}` очков). \n\n"
    if best_hand_fu > 0:
        message += f"Лучшая рука: `{best_hand_fu}` хан. \n\n"
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
    return message

# from datetime import datetime
import datetime

from django.core.management import BaseCommand
from django.utils import timezone

from website.games.models import Game


class Command(BaseCommand):

    def handle(self, *args, **options):
        games = Game.objects.all()

        for game in games:
            game_date = game.external_id.split('-')[0]
            game_date = datetime.datetime.strptime(game_date, '%Y%m%d%Hgm').replace(tzinfo=timezone.utc)

            game.game_place = Game.TENHOU
            game.game_type = Game.FOUR_PLAYERS
            game.game_rule = Game.HANCHAN_TANYAO_RED_FIVES
            game.game_date = game_date

            game.save()

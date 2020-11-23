from django.core.management import BaseCommand
from tqdm import tqdm

from api.views import _load_log_and_update_game
from website.accounts.models import Player
from website.games.models import Game, GameRound


class Command(BaseCommand):

    def handle(self, *args, **options):
        players = Player.objects.all()

        for player in tqdm(players, position=0):
            games = player.games.filter(status=Game.FINISHED)

            for game in tqdm(games, position=1):
                GameRound.objects.filter(game=game).delete()
                _load_log_and_update_game(game)

import tarfile

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from tqdm import tqdm
from api.views import _load_log_and_update_game
from website.accounts.models import Player
from website.games.models import Game


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('replays_path', type=str)

    def handle(self, *args, **options):
        # hardcode it for now
        players = []
        player_names = ["Ichihime", "Kaavi", "Xenia", "Wanjirou"]
        user = User.objects.get(username='admin')
        for player_name in player_names:
            players.append(Player.objects.get_or_create(user=user, username=player_name)[0])

        # erase old state
        Game.objects.all().delete()

        tar = tarfile.open(options['replays_path'], "r:gz")
        for member in tqdm(tar.getmembers()):
            f = tar.extractfile(member)
            if f is None:
                continue

            content = f.read()
            if not content:
                continue

            log_id = member.name[2:].split('.')[0]

            games = []
            for player in players:
                games.append(
                    Game.objects.create(
                        player=player,
                        external_id=log_id,
                        status=Game.STARTED,
                        game_log_content=content
                    )
                )

            for game in games:
                try:
                    _load_log_and_update_game(game)
                except Exception:
                    print(f"Error {log_id}")

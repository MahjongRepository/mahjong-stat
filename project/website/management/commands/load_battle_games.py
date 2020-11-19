import csv
import statistics
import tarfile

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from tqdm import tqdm
from api.views import _load_log_and_update_game
from website.accounts.models import Player
from website.games.models import Game
from django.db.models import Avg


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

        i = 0
        results = []
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
                    Game(
                        player=player,
                        external_id=log_id,
                        status=Game.STARTED,
                        game_log_content=content.decode('utf-8')
                    )
                )

            for game in games:
                try:
                    _load_log_and_update_game(game)
                except Exception as e:
                    print(f"Error {log_id}")

            if i % 100 == 0:
                result_item = {
                    'games': i,
                }
                avgs = []
                for player in players:
                    games = Game.objects.filter(player=player).order_by()
                    average_position = games.aggregate(Avg('player_position'))['player_position__avg']
                    avgs.append(average_position)
                    result_item[player.username] = average_position

                result_item['dispersion'] = max(avgs) - min(avgs)
                result_item['variation_25'] = max(abs(max(avgs) - 2.5), abs(min(avgs) - 2.5))
                result_item['stdev'] = statistics.stdev(avgs)
                results.append(result_item)

            i += 1

        with open('results.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
            writer.writeheader()
            for data in results:
                writer.writerow(data)

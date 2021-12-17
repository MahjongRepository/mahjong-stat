import csv
import statistics
import tarfile

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from tqdm import tqdm
from api.views import _load_log_and_update_game
from website.accounts.models import Player
from website.games.models import Game


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("replays_path", type=str)

    def handle(self, *args, **options):
        # hardcode it for now
        players = []
        player_names = ["Washizu", "Akagi", "Ichihime", "Miki"]
        user = User.objects.get(username="admin")
        for player_name in player_names:
            players.append(Player.objects.get_or_create(user=user, username=player_name)[0])

        # erase old state
        Game.objects.all().delete()

        i = 0
        results = []
        tar = tarfile.open(options["replays_path"], "r:gz")
        player_stat = {}
        for member in tqdm(tar.getmembers()):
            f = tar.extractfile(member)
            if f is None:
                continue

            content = f.read()
            if not content:
                continue

            log_id = member.name[2:].split(".")[0]
            try:
                games = []
                for player in players:
                    games.append(
                        Game(
                            player=player,
                            external_id=log_id,
                            status=Game.STARTED,
                            game_log_content=content.decode("utf-8"),
                        )
                    )

                for game in games:
                    _, player_data = _load_log_and_update_game(game)
                    if game.player.username not in player_stat:
                        player_stat[game.player.username] = {"places": [], "scores": []}
                    player_stat[game.player.username]["places"].append(player_data["position"])
                    player_stat[game.player.username]["scores"].append(player_data["scores"])
            except Exception as e:
                print(f"Error {log_id}")

            if i % 100 == 0:
                result_item = {
                    "games": i,
                }

                avgs = []
                for player in players:
                    username = player.username

                    average_position = sum(player_stat[username]["places"]) / len(
                        player_stat[player.username]["places"]
                    )
                    avgs.append(average_position)

                    dan_3_pt = sum(
                        [60 for x in player_stat[username]["places"] if x == 1]
                        + [15 for x in player_stat[username]["places"] if x == 2]
                        + [-75 for x in player_stat[username]["places"] if x == 4]
                    )

                    dan_3_pt = (dan_3_pt / len(player_stat[username]["places"])) * 100
                    avg_scores = sum(player_stat[username]["scores"]) / len(player_stat[username]["scores"])

                    result_item[username] = average_position
                    result_item[f"{username} pt"] = int(dan_3_pt)
                    result_item[f"{username} scores"] = int(avg_scores)

                result_item["dispersion"] = max(avgs) - min(avgs)
                result_item["variation_25"] = max(abs(max(avgs) - 2.5), abs(min(avgs) - 2.5))
                result_item["stdev"] = statistics.stdev(avgs)

                results.append(result_item)

            i += 1

        with open("results.csv", "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
            writer.writeheader()
            for data in results:
                writer.writerow(data)

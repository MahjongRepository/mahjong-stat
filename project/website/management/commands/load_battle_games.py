import csv
import itertools
import re
import statistics
import tarfile

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from tqdm import tqdm
from api.views import _load_log_and_update_game
from parsers.tenhou.main import TenhouLogParser
from website.accounts.models import Player
from website.games.models import Game


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("replays_path", type=str)

    def handle(self, *args, **options):
        # hardcode it for now
        players = []
        player_names = [
            "Ichihime",
            "Kaavi",
            "Xenia",
            "Wanjirou",
            "Miki",
            "Chiori",
            "Kana",
            "Mai",
            "Yui",
            "Nadeshiko",
            "Riu",
            "Keikumusume",
        ]

        one_tour_tables = list(itertools.combinations(player_names, 4))
        assert len(one_tour_tables) == 495

        user = User.objects.get(username="admin")
        for player_name in player_names:
            players.append(Player.objects.get_or_create(user=user, username=player_name)[0])

        # erase old state
        Game.objects.all().delete()

        tar = tarfile.open(options["replays_path"], "r:gz")
        regex = r"(<UN.*)<TAIKYOKU"
        parser = TenhouLogParser()
        games_configurations = {}
        for member in tqdm(tar.getmembers()):
            f = tar.extractfile(member)
            if f is None:
                continue

            content = f.read()
            if not content:
                continue

            log_id = member.name[2:].split(".")[0]
            try:
                log_content = content.decode("utf-8")
                search = re.search(regex, log_content, re.MULTILINE)
                names_tag = search.group(1)
                names = sorted(parser.parse_names(names_tag))

                key = ".".join(names)
                if key not in games_configurations:
                    games_configurations[key] = []

                games_configurations[key].append(
                    {"log_id": log_id, "log_content": log_content, "names": names,}
                )
            except Exception as e:
                print(f"Error {log_id}")

        min_games = 1000
        for key in games_configurations.keys():
            if len(games_configurations[key]) < min_games:
                min_games = len(games_configurations[key])

        # make sure that all bots played same number of games
        for key in games_configurations.keys():
            games_configurations[key] = games_configurations[key][:min_games]

        results = []
        player_stat = {}

        for tour in tqdm(range(min_games)):
            for key in games_configurations.keys():
                game_data = games_configurations[key][tour]

                try:
                    games = []
                    for player in players:
                        if player.username not in game_data["names"]:
                            continue

                        games.append(
                            Game(
                                player=player,
                                external_id=game_data["log_id"],
                                status=Game.STARTED,
                                game_log_content=game_data["log_content"],
                            )
                        )

                    for game in games:
                        _, player_data = _load_log_and_update_game(game)
                        if game.player.username not in player_stat:
                            player_stat[game.player.username] = {"places": [], "scores": []}
                        player_stat[game.player.username]["places"].append(player_data["position"])
                        player_stat[game.player.username]["scores"].append(player_data["scores"])
                except Exception as e:
                    print(f"Error {game_data['log_id']}")

            result_item = {
                "tour": tour + 1,
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

        with open("results.csv", "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
            writer.writeheader()
            for data in results:
                writer.writerow(data)

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from website.accounts.models import Player
from website.games.models import Game
from website.games.views import _build_stat


class Command(BaseCommand):

    def handle(self, *args, **options):
        # hardcode it for now
        players = []
        player_names = ["Washizu", "Akagi", "Ichihime", "Miki"]
        user = User.objects.get(username="admin")
        for player_name in player_names:
            players.append(Player.objects.get_or_create(user=user, username=player_name)[0])

        response_data = {}
        for player in players:
            games = player.games.filter(status=Game.FINISHED).order_by("-game_date", "-id")
            stat_data = {
                "player": player,
            }
            stat_data.update(_build_stat(games, [player], "all"))

            del stat_data['player']
            del stat_data['games']
            del stat_data['latest_rank']
            del stat_data['latest_rate']
            del stat_data['room_filters']
            del stat_data['room_filter']
            response_data[player.username] = stat_data

        header = [""]
        header.extend(response_data.keys())
        csv_data = [
            header
        ]
        stat_keys = list(response_data.values())[0].keys()
        for stat_key in stat_keys:
            row = [stat_key]
            for player_key in response_data.keys():
                row.append(response_data[player_key][stat_key])
            csv_data.append(row)

        for x in csv_data:
            print(",".join([str(y) for y in x]))


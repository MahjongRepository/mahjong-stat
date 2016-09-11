from django.core.management import BaseCommand

from tenhou_log_parser.main import TenhouLogParser
from website.accounts.models import Player
from website.games.models import Game, GameRound


class Command(BaseCommand):

    def handle(self, *args, **options):
        players = Player.objects.all()

        for player in players:
            games = player.games.all()

            for game in games:
                GameRound.objects.filter(game=game).delete()

                results = TenhouLogParser().parse_log(game.external_id, game.game_log_content)
                player_result = next((i for i in results['players'] if i['name'] == player.username), None)

                game.player_position = player_result['position']
                game.scores = player_result['scores']
                game.seat = player_result['seat']
                game.game_rule = results['game_rule']
                game.game_type = results['game_type']
                game.game_date = results['game_date']
                game.lobby = results['lobby']
                game.save()

                for round_data in player_result['rounds']:
                    GameRound.objects.create(
                        game=game,
                        is_win=round_data['is_win'],
                        is_deal=round_data['is_deal'],
                        is_retake=round_data['is_retake'],
                        is_tsumo=round_data['is_tsumo'],
                        is_riichi=round_data['is_riichi'],
                        is_open_hand=round_data['is_open_hand'],
                        is_damaten=round_data['is_damaten'],
                        round_number=round_data['round_number'],
                        honba=round_data['honba'],
                        win_scores=round_data['win_scores'],
                        lose_scores=round_data['lose_scores'],
                    )

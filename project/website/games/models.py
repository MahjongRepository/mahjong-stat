from django.db import models

from tenhou_log_parser.constants import MahjongConstants
from website.accounts.models import User, Player


class Game(models.Model, MahjongConstants):
    REAL_LIFE = 1
    TENHOU = 2
    GAMES = (
        (REAL_LIFE, 'Real life game record'),
        (TENHOU, 'Tenhou game'),
    )

    player = models.ForeignKey(Player, related_name='games')

    game_place = models.PositiveSmallIntegerField(choices=GAMES, default=TENHOU)
    game_rule = models.PositiveSmallIntegerField(choices=MahjongConstants.GAME_RULES, default=MahjongConstants.UNKNOWN)
    game_type = models.PositiveSmallIntegerField(choices=MahjongConstants.GAME_TYPES, default=MahjongConstants.UNKNOWN)
    lobby = models.PositiveSmallIntegerField(default=0)
    game_date = models.DateTimeField(default=None, null=True, blank=True)

    # let's store all games contents
    # to be able rebuild statistics in future without a lot of downloads from tenhou servers
    game_log_content = models.TextField()

    external_id = models.CharField(max_length=255, default='', null=True, blank=True)
    player_position = models.PositiveSmallIntegerField(default=0)
    scores = models.SmallIntegerField(default=0)
    seat = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mahjong_game'
        ordering = ['-game_date']

    def get_tenhou_url(self):
        seat = self.seat - 1
        return 'http://tenhou.net/0/?log={0}&tw={1}'.format(self.external_id, seat)

from django.db import models

from website.accounts.models import User, Player


class Game(models.Model):
    REAL_LIFE = 0
    TENHOU = 1
    GAMES = (
        (REAL_LIFE, 'Real life game record'),
        (TENHOU, 'Tenhou game'),
    )

    FOUR_PLAYERS = 0
    THREE_PLAYERS = 1
    GAME_TYPES = (
        (FOUR_PLAYERS, 'Standard game'),
        (THREE_PLAYERS, 'Hirosima'),
    )

    TONPUSEN_ARI_ARI = 0
    HANCHAN_ARI_ARI = 1
    GAME_RULES = (
        (TONPUSEN_ARI_ARI, 'Tonpu-sen. Ari, Ari.'),
        (HANCHAN_ARI_ARI, 'Hanchan. Ari, Ari.'),
    )

    player = models.ForeignKey(Player, related_name='games')

    game = models.PositiveSmallIntegerField(choices=GAMES, default=TENHOU)
    game_rule = models.PositiveSmallIntegerField(choices=GAME_RULES, default=TONPUSEN_ARI_ARI)
    game_type = models.PositiveSmallIntegerField(choices=GAME_TYPES, default=FOUR_PLAYERS)

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
        ordering = ['-created_at']

    def get_tenhou_url(self):
        seat = self.seat - 1
        return 'http://tenhou.net/0/?log={0}&tw={1}'.format(self.external_id, seat)

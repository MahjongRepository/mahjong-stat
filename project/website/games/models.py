from django.db import models

from website.accounts.models import User, Player


class Game(models.Model):
    REAL_LIFE = 0
    TENHOU = 1

    TYPES = (
        (REAL_LIFE, 'Real life game record'),
        (TENHOU, 'Tenhou.net log'),
    )

    TONPUSEN_ARI_ARI = 0
    HANCHAN_ARI_ARI = 0
    RULES = (
        (TONPUSEN_ARI_ARI, 'Tonpu-sen. Ari, Ari.'),
        (HANCHAN_ARI_ARI, 'Hanchan. Ari, Ari.'),
    )

    player = models.ForeignKey(Player, related_name='games')
    type = models.PositiveSmallIntegerField(choices=TYPES, default=TENHOU)
    game_rule = models.PositiveSmallIntegerField(choices=RULES, default=TONPUSEN_ARI_ARI)

    external_id = models.TextField(default='', null=True, blank=True)
    player_position = models.PositiveSmallIntegerField(default=0)
    scores = models.SmallIntegerField(default=0)
    seat = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mahjong_game'
        ordering = ['-created_at']

    def get_tenhou_url(self):
        return 'http://tenhou.net/0/?log={0}&tw={1}'.format(self.external_id, self.seat)

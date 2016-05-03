from django.db import models

from website.accounts.models import User


class Game(models.Model):
    REAL_LIFE = 0
    TENHOU = 1

    TYPES = (
        (REAL_LIFE, 'Real life game record'),
        (TENHOU, 'Tenhou.net log'),
    )

    user = models.ForeignKey(User)
    type = models.PositiveSmallIntegerField(choices=TYPES, default=TENHOU)
    external_id = models.TextField(default='', null=True, blank=True)
    player_position = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mahjong_game'
        ordering = ['-created_at']

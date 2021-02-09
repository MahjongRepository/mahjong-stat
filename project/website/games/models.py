from django.db import models

from parsers.tenhou.constants import MahjongConstants
from website.accounts.models import Player


class Game(models.Model, MahjongConstants):
    STARTED = 0
    FINISHED = 1
    STATUSES = [
        [STARTED, 'Started'],
        [FINISHED, 'Finished'],
    ]

    player = models.ForeignKey(Player, related_name='games', on_delete=models.CASCADE)

    game_rule = models.PositiveSmallIntegerField(choices=MahjongConstants.GAME_RULES, default=MahjongConstants.UNKNOWN)
    game_type = models.PositiveSmallIntegerField(choices=MahjongConstants.GAME_TYPES, default=MahjongConstants.UNKNOWN)
    lobby = models.PositiveSmallIntegerField(default=0)
    game_room = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    game_date = models.DateTimeField(default=None, null=True, blank=True)

    status = models.PositiveSmallIntegerField(choices=STATUSES)

    # let's store all games contents
    # to be able rebuild statistics in future without a lot of downloads from tenhou servers
    game_log_content = models.TextField(null=True, blank=True)

    external_id = models.CharField(max_length=255, default='', null=True, blank=True)
    player_position = models.PositiveSmallIntegerField(default=0)
    scores = models.IntegerField(default=0)
    seat = models.PositiveSmallIntegerField(default=0)
    rate = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    rank = models.PositiveIntegerField(choices=MahjongConstants.RANKS, default=MahjongConstants.NEWBIE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mahjong_game'
        ordering = ['-game_date']

    def get_tenhou_url(self):
        return 'http://tenhou.net/3/?log={0}&tw={1}'.format(self.external_id, self.seat)


class GameRound(models.Model):
    game = models.ForeignKey(Game, related_name='rounds', on_delete=models.CASCADE)

    is_win = models.BooleanField(default=False)
    # deal to ron
    is_deal = models.BooleanField(default=False)
    is_retake = models.BooleanField(default=False)

    is_tsumo = models.BooleanField(default=False)
    is_riichi = models.BooleanField(default=False)
    is_open_hand = models.BooleanField(default=False)
    is_damaten = models.BooleanField(default=False)

    round_number = models.PositiveSmallIntegerField(default=0)
    honba = models.PositiveSmallIntegerField(default=0)

    # use it for direct link to the game round
    round_counter = models.PositiveSmallIntegerField(default=0)

    han = models.PositiveSmallIntegerField(default=0)
    fu = models.PositiveSmallIntegerField(default=0)

    win_scores = models.PositiveIntegerField(default=0)
    lose_scores = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mahjong_game_round'
        ordering = ['round_number', 'honba']

    def round_number_display(self):
        rounds = [u'東', u'南', u'西', u'北']
        return '{0}{1}'.format(rounds[self.round_number // 4], self.round_number + 1)

    def get_tenhou_url_for_round(self):
        return self.game.get_tenhou_url() + f'&ts={self.round_counter}'

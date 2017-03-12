import json

from django.db import models

from website.accounts.models import Player


class MahjongEvent(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mahjong_event'


class EventPlayer(models.Model):
    player = models.ForeignKey(Player)
    event = models.ForeignKey(MahjongEvent)

    average_place = models.DecimalField(decimal_places=2, max_digits=4, default=0)
    rate = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    sum_of_places = models.PositiveIntegerField(default=0)
    played_games = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mahjong_event_player'


class EventGame(models.Model):
    event = models.ForeignKey(MahjongEvent)

    external_id = models.CharField(max_length=255)
    game_date = models.DateTimeField(default=None, null=True, blank=True)
    result = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mahjong_event_game'

    def tenhou_link(self):
        return 'http://tenhou.net/0/?log={}'.format(self.external_id)

    def parsed_result(self):
        return json.loads(self.result)

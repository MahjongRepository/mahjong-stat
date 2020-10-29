from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from website.games.models import Game, GameRound


class GameAdmin(admin.ModelAdmin):
    search_fields = ['external_id']
    ordering = ['-updated_at']
    list_filter = ['player__username', 'status']
    list_display = ['id', 'player', 'place', 'scores', 'status', 'updated_at', 'action']

    def place(self, obj):
        return obj.player_position

    def action(self, obj):
        if obj.status == Game.STARTED:
            url = reverse('manually_load_results', kwargs={'game_id': obj.id})
            return format_html(f'<a href="{url}">Load results</a>')
        return ''

    def player(self, obj):
        url = reverse('player_statistics', kwargs={'player_name': obj.player.username})
        return format_html(f'<a href="{url}" target="_blank">{obj.player.username}</a>')


class GameRoundAdmin(admin.ModelAdmin):
    list_display = ['id', 'player', 'game_link', 'win_scores', 'lose_scores', 'han', 'fu', 'date']
    list_filter = ['game__game_date', 'is_win', 'is_deal']
    ordering = ['game__game_date']

    def player(self, obj):
        username = obj.game.player.username
        url = reverse('player_statistics', kwargs={'player_name': username})
        return format_html(f'<a href="{url}" target="_blank">{username}</a>')

    def game_link(self, obj):
        return format_html(f'<a href="{obj.get_tenhou_url_for_round()}" target="_blank">link</a>')

    def date(self, obj):
        return obj.game.game_date


admin.site.register(Game, GameAdmin)
admin.site.register(GameRound, GameRoundAdmin)

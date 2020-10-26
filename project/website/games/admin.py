from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from website.games.models import Game


class GameAdmin(admin.ModelAdmin):
    search_fields = ['external_id']
    ordering = ['-updated_at']
    list_filter = ['player__username', 'status']
    list_display = ['id', 'player_link', 'place', 'scores', 'status', 'created_at', 'updated_at', 'action']

    def place(self, obj):
        return obj.player_position

    def action(self, obj):
        if obj.status == Game.STARTED:
            url = reverse('manually_load_results', kwargs={'game_id': obj.id})
            return format_html(f'<a href="{url}">Load results</a>')
        return ''

    def player_link(self, obj):
        url = reverse('player_statistics', kwargs={'player_name': obj.player.username})
        return format_html(f'<a href="{url}" target="_blank">{obj.player.username}</a>')


admin.site.register(Game, GameAdmin)

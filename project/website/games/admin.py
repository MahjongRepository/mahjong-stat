from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from website.games.models import Game


class GameAdmin(admin.ModelAdmin):
    search_fields = ['external_id']
    ordering = ['-created_at']
    list_filter = ['status']
    list_display = ['player', 'player_position', 'scores', 'status', 'created_at', 'action']

    def action(self, obj):
        if obj.status == Game.STARTED:
            url = reverse('manually_load_results', kwargs={'game_id': obj.id})
            return format_html(f'<a href="{url}">Load results</a>')
        return ''


admin.site.register(Game, GameAdmin)

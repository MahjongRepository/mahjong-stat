from django.contrib import admin

from website.games.models import Game


class GameAdmin(admin.ModelAdmin):
    search_fields = ['external_id']
    ordering = ['-created_at']
    list_filter = ['status']
    list_display = ['player', 'player_position', 'scores', 'status', 'created_at']


admin.site.register(Game, GameAdmin)

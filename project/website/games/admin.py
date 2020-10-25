from django.contrib import admin

from website.games.models import Game


class GameAdmin(admin.ModelAdmin):
    list_filter = ('status', )
    list_display = ('player', 'game_rule', 'player_position', 'scores', 'status', 'created_at')

admin.site.register(Game, GameAdmin)

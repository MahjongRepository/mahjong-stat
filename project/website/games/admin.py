from django.contrib import admin

from website.games.models import Game


class GameAdmin(admin.ModelAdmin):
    list_display = ('player', 'type', 'player_position', 'scores', 'created_at')

admin.site.register(Game, GameAdmin)

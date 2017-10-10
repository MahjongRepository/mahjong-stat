from django.contrib import admin

from website.accounts.models import Player


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('username', 'created_at')


admin.site.register(Player, PlayerAdmin)

from django.contrib import admin

from website.events.models import MahjongEvent, EventPlayer, EventGame


class MahjongEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class EventPlayerAdmin(admin.ModelAdmin):
    list_display = ('player', 'average_place', 'rate')


class EventGameAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'result')

admin.site.register(MahjongEvent, MahjongEventAdmin)
admin.site.register(EventPlayer, EventPlayerAdmin)
admin.site.register(EventGame, EventGameAdmin)

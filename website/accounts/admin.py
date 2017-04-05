from django.contrib import admin

from website.accounts.models import User, Player


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_joined')


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('username', 'created_at')

admin.site.register(User, UserAdmin)
admin.site.register(Player, PlayerAdmin)

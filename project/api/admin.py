from django.contrib import admin

from api.models import ApiToken


class ApiTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'user', 'created_at')

admin.site.register(ApiToken, ApiTokenAdmin)

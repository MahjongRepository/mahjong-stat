# from datetime import datetime
import datetime

from django.core.management import BaseCommand
from django.utils import timezone

from website.games.models import Game


class Command(BaseCommand):

    def handle(self, *args, **options):
        games = Game.objects.all()

        for game in games:
            game.seat -= 1
            game.save()

from time import sleep

import os
import requests

from django.core.management import BaseCommand

from website.games.models import Game


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('token', type=str)
        parser.add_argument('host', type=str)
        parser.add_argument('meta_file', type=str)
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        url = '{}/api/v1/tenhou/game/add/'.format(options['host'])
        token = options['token']
        meta_file = options['meta_file']
        username = options['username']

        records_to_add = []
        if os.path.exists(meta_file):
            with open(meta_file, 'r', encoding='utf-8') as f:
                records_to_add = f.read().split('\n')

        for item in records_to_add:
            game_id = item.split('&')[0].split('=')[1]
            requests.post(url, {'id': game_id, 'username': username}, headers={'Token': token})
            print('Added {}'.format(game_id))

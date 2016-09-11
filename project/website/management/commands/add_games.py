from time import sleep

import os
import requests

from django.core.management import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('meta_file', type=str)
        parser.add_argument('token', type=str)

    def handle(self, *args, **options):
        url = 'http://localhost:8000/api/v1/tenhou/game/add/'
        token = options['token']
        meta_file = options['meta_file']

        records_to_add = []
        if os.path.exists(meta_file):
            with open(meta_file, 'r', encoding='utf-8') as f:
                records_to_add = f.read().split('\n')

        i = 0
        count = len(records_to_add)
        for item in records_to_add:
            game_id = item.split('&')[0].split('=')[1]

            requests.post(url, {'id': game_id}, headers={'Token': token})

            i += 1
            sleep(1)
            print('{0}/{1}'.format(i, count))

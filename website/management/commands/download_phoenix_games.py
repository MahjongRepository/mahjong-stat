import glob
import gzip

import os
import requests
from django.conf import settings

from django.core.management import BaseCommand


class Command(BaseCommand):

    def __init__(self):
        super().__init__()

        self.logs_temp_directory = os.path.join(settings.BASE_DIR, 'phoenix_data')
        if not os.path.exists(self.logs_temp_directory):
            os.mkdir(self.logs_temp_directory)

    def handle(self, *args, **options):

        self.download_archives('http://tenhou.net/sc/raw/list.cgi?old')
        self.download_archives('http://tenhou.net/sc/raw/list.cgi')

        player_statistics = self.collect_players_statistics()
        player_statistics = sorted(player_statistics.items(), key=lambda x: x[1]['games'], reverse=True)

        for item in player_statistics[:10]:
            print(item[0], item[1]['games'])

    def download_archives(self, items_url):
        download_url = 'http://tenhou.net/sc/raw/dat/'

        response = requests.get(items_url)
        response = response.text.replace('list(', '').replace(');', '')
        response = response.split(',\r\n')
        for archive_name in response:
            if 'scc' in archive_name:
                archive_name = archive_name.split("',")[0].replace("{file:'", '')

                file_name = archive_name
                if '/' in file_name:
                    file_name = file_name.split('/')[1]
                archive_path = os.path.join(self.logs_temp_directory, file_name)

                if not os.path.exists(archive_path):
                    print('Downloading... {}'.format(archive_name))

                    url = '{}{}'.format(download_url, archive_name)
                    page = requests.get(url)
                    with open(archive_path, 'wb') as f:
                        f.write(page.content)

    def collect_players_statistics(self):
        player_statistics = {}
        gz_files = glob.glob('{}/*.gz'.format(self.logs_temp_directory))
        for gz_file in gz_files:
            with gzip.open(gz_file, 'r') as f:
                for line in f:
                    result = str(line, 'utf-8').split('|')

                    game_type = result[2].strip()
                    game_id = result[3].split('log=')[1][:31]
                    players = result[4].split(' ')[1:]
                    for x in range(0, len(players)):
                        players[x] = players[x].split('(')[0]

                    for player in players:
                        if player in player_statistics:
                            player_statistics[player]['games'] += 1
                        else:
                            player_statistics[player] = {}
                            player_statistics[player]['games'] = 1
                            player_statistics[player]['logs'] = []

                        player_statistics[player]['logs'].append(game_id)

        return player_statistics

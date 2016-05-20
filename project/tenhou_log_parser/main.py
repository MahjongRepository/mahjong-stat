from urllib.parse import unquote
from urllib.request import urlopen

import codecs
import os
import struct
from bs4 import BeautifulSoup
from django.conf import settings

logs_temp_directory = os.path.join(settings.BASE_DIR, 'tests_temp_data')


class TenhouLogParser(object):

    def parse_log(self, log_id):
        player_names = []
        scores = []

        log_data = self._get_log_data(log_id)

        # tenhou produced not valid XML, so let's use BeautifulSoup for parsing
        soup = BeautifulSoup(log_data, 'html.parser')
        elements = soup.find_all()
        for tag in elements:
            if tag.name == 'un' and 'rate' in tag.attrs:
                player_names = self.parse_names(tag)

            if 'owari' in tag.attrs:
                scores, _ = self.parse_final_scored(tag)

        players = []
        for i in range(0, len(player_names)):
            players.append({'name': player_names[i], 'scores': int(scores[i] * 100), 'seat': i + 1})

        players = sorted(players, key=lambda x: x['scores'], reverse=True)
        for i in range(0, len(players)):
            players[i]['position'] = i + 1

        return {'players': players, 'log_data': log_data}

    def parse_names(self, tag):
        return [
            unquote(tag.attrs['n0']),
            unquote(tag.attrs['n1']),
            unquote(tag.attrs['n2']),
            unquote(tag.attrs['n3'])
        ]

    def parse_final_scored(self, tag):
        data = tag.attrs['owari']
        data = [float(i) for i in data.split(',')]

        # start at the beginning at take every second item (even)
        scores = data[::2]
        # start at second item and take every second item (odd)
        uma = data[1::2]

        return scores, uma

    def _get_log_data(self, log_id):
        if not os.path.exists(logs_temp_directory):
            os.mkdir(logs_temp_directory)

        log_file = os.path.join(logs_temp_directory, log_id + '.xml')

        if os.path.exists(log_file):
            log_file = open(log_file, 'r')
            log_data = log_file.read()
            log_file.close()
        else:
            log_id = self._get_log_name_for_download(log_id)
            log_data = self._download_log(log_id)

            with open(log_file, 'wb') as f:
                f.write(log_data)

        return log_data

    def _download_log(self, log_id):
        resp = urlopen('http://e.mjv.jp/0/log/?' + log_id)
        data = resp.read()
        return data

    def _get_log_name_for_download(self, log_id):
        table = [
            22136, 52719, 55146, 42104,
            59591, 46934, 9248,  28891,
            49597, 52974, 62844, 4015,
            18311, 50730, 43056, 17939,
            64838, 38145, 27008, 39128,
            35652, 63407, 65535, 23473,
            35164, 55230, 27536, 4386,
            64920, 29075, 42617, 17294,
            18868, 2081
        ]

        code_pos = log_id.rindex("-") + 1
        code = log_id[code_pos:]
        if code[0] == 'x':
            a, b, c = struct.unpack(">HHH", bytes.fromhex(code[1:]))
            index = 0
            if log_id[:12] > "2010041111gm":
                x = int("3" + log_id[4:10])
                y = int(log_id[9])
                index = x % (33 - y)
            first = (a ^ b ^ table[index]) & 0xFFFF
            second = (b ^ c ^ table[index] ^ table[index + 1]) & 0xFFFF
            return log_id[:code_pos] + codecs.getencoder('hex_codec')(struct.pack(">HH", first, second))[0].decode('ASCII')
        else:
            return log_id

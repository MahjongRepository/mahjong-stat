import re
from datetime import datetime
from urllib.parse import unquote
from urllib.request import urlopen

import codecs
import os
import struct
from django.conf import settings
from django.utils import timezone

from parsers.tenhou.constants import MahjongConstants
from parsers.tenhou.meld import Meld

logs_temp_directory = os.path.join(settings.BASE_DIR, 'tests_temp_data')


class TenhouLogParser(MahjongConstants):

    def parse_log(self, log_id, log_data=None):
        player_names = []
        player_rates = []
        player_ranks = []
        scores = []
        lobby = 0
        game_room = self.UNKNOWN
        game_rule = self.UNKNOWN
        rounds = []

        if not log_data:
            log_data = self._get_log_data(log_id)

        game_date = log_id.split('-')[0]
        # 2016052113gm
        if 'gm' in game_date:
            game_date = datetime.strptime(game_date, '%Y%m%d%Hgm').replace(tzinfo=timezone.utc)
        else:  # local games battle
            game_date = datetime.utcnow().replace(tzinfo=timezone.utc)

        parsed_rounds = self.split_log_to_game_rounds(log_data)

        round_data = {}
        win_scores = {}
        lose_scores = {}
        who_open_hand = []
        who_called_riichi = []
        round_number = 0
        honba = 0

        for round_data_item in parsed_rounds:
            for tag in round_data_item:
                if self.is_init_tag(tag):
                    seed = self.get_attribute_content(tag, 'seed').split(',')
                    seed = [int(i) for i in seed]

                    round_number = seed[0]
                    honba = seed[1]

                if "<UN" in tag and "dan" in tag:
                    player_names = self.parse_names(tag)
                    player_rates = self.parse_rates(tag)
                    player_ranks = self.parse_ranks(tag)

                # start of the game
                if "<GO" in tag:
                    lobby, game_rule, game_room = self.parse_game_lobby_and_rule(tag)

                # someone is win
                if self.is_agari_tag(tag):
                    winner = int(self.get_attribute_content(tag, 'who'))
                    from_who = int(self.get_attribute_content(tag, 'fromWho'))

                    ten = self.get_attribute_content(tag, 'ten').split(',')
                    ten = [int(i) for i in ten]

                    win_scores[winner] = ten[1]
                    # in double ron we need to calculate all dealt hands
                    if from_who != winner:
                        if from_who in lose_scores:
                            lose_scores[from_who] += ten[1]
                        else:
                            lose_scores[from_who] = ten[1]

                    # format: sc="157,20,245,-39,376,-79,222,-39"
                    if self.get_attribute_content(tag, 'sc'):
                        scores = self.get_attribute_content(tag, 'sc').split(',')
                        scores = [int(i) for i in scores]

                        seat = 0
                        scores = scores[1::2]
                        for score in scores:
                            score *= 100
                            if score > 0:
                                win_scores[seat] = score
                            else:
                                lose_scores[seat] = score * -1
                            seat += 1

                    han = 0
                    fu = ten[0]
                    if self.get_attribute_content(tag, 'yaku'):
                        han = sum([int(x) for x in self.get_attribute_content(tag, 'yaku').split(',')[1::2]])

                    if self.get_attribute_content(tag, 'yakuman'):
                        # TODO save real yakuman value
                        han = 13

                    if round_data:
                        round_data['winners'].append(winner)
                    else:
                        round_data = {
                            'winners': [winner],
                            'from_who': from_who,
                            'who_open_hand': who_open_hand,
                            'who_called_riichi': who_called_riichi,
                            'is_retake': False,
                            'round_number': round_number,
                            'honba': honba,
                            'win_scores': win_scores,
                            'lose_scores': lose_scores,
                            'han': han,
                            'fu': fu,
                        }

                # retake
                if "<RYUUKYOKU" in tag:
                    round_data = {
                        'is_retake': True,
                        'round_number': round_number,
                        'who_called_riichi': who_called_riichi,
                        'who_open_hand': who_open_hand,
                        'honba': honba,
                    }

                if "<N who=" in tag:
                    meld = self.parse_meld(tag)
                    if meld.opened:
                        who_open_hand.append(int(meld.who))

                if "<REACH" in tag and 'step="1"' in tag:
                    who_called_riichi.append(int(self.get_attribute_content(tag, 'who')))

                # because of double ron, we can push round information
                # after new round started
                # or after the end of game
                if round_data and (self.is_init_tag(tag) or 'owari' in tag):
                    rounds.append(round_data)
                    round_data = {}
                    win_scores = {}
                    lose_scores = {}
                    who_open_hand = []
                    who_called_riichi = []

                # the final results
                if 'owari' in tag:
                    scores, _ = self.parse_final_scores(tag)

        if not scores:
            scores = [0] * len(player_names)

        players = []
        for player_seat in range(0, len(player_names)):
            player_rounds = []

            for round_data in rounds:
                data = {
                    'is_win': False,
                    'is_deal': False,
                    'is_tsumo': False,
                    'is_retake': False,
                    'is_open_hand': round_data.get('who_open_hand') and player_seat in round_data['who_open_hand'] or False,
                    'is_riichi': round_data.get('who_called_riichi') and player_seat in round_data['who_called_riichi'] or False,
                    'is_damaten': False,
                    'round_number': round_data['round_number'],
                    'honba': round_data['honba'],
                    'han': round_data.get('han', 0),
                    'fu': round_data.get('fu', 0),
                    'win_scores': 0,
                    'lose_scores': 0,
                }

                if round_data['is_retake']:
                    data['is_retake'] = True
                else:
                    is_winner = player_seat in round_data['winners']
                    is_loser = round_data['from_who'] not in round_data['winners'] and round_data['from_who'] == player_seat

                    data['is_win'] = is_winner
                    data['is_deal'] = is_loser
                    data['is_tsumo'] = is_winner and round_data['from_who'] in round_data['winners']
                    data['is_damaten'] = data['is_win'] and not data['is_riichi'] and not data['is_open_hand']
                    data['win_scores'] = player_seat in round_data['win_scores'] and round_data['win_scores'][player_seat] or 0
                    data['lose_scores'] = player_seat in round_data['lose_scores'] and round_data['lose_scores'][player_seat] or 0

                player_rounds.append(data)

            players.append({
                'name': player_names[player_seat],
                'rate': player_rates[player_seat],
                'rank': player_ranks[player_seat],
                'scores': int(scores[player_seat] * 100),
                'seat': player_seat,
                'rounds': player_rounds
            })

        players = sorted(players, key=lambda x: x['scores'], reverse=True)
        for player_seat in range(0, len(players)):
            players[player_seat]['position'] = player_seat + 1

        game_type = self.FOUR_PLAYERS
        if len(players) == 3:
            game_type = self.THREE_PLAYERS

        return {
            'lobby': lobby,
            'game_room': game_room,
            'game_type': game_type,
            'game_rule': game_rule,
            'players': players,
            'log_data': log_data,
            'game_date': game_date
        }

    def parse_game_lobby_and_rule(self, tag):
        lobby = int(self.get_attribute_content(tag, 'lobby'))
        game_rule_temp = int(self.get_attribute_content(tag, 'type'))

        """
          0 - 1 - online, 0 - bots
          1 - aka
          2 - kuitan forbiden
          3 - hanchan
          4 - 3man
          5 - dan flag
          6 - fast game
          7 - dan flag
          Combine them as:
          76543210
          00001001 = 9 = hanchan ari-ari
          00000001 = 1 = tonpu-sen ari-ari
        """
        rule = bin(game_rule_temp).replace('0b', '')
        while len(rule) != 8:
            rule = '0' + rule

        is_hanchan = rule[4] == '1'
        is_aka = rule[7] == '1'
        is_open_tanyao = rule[6] == '0'
        is_fast = rule[1] == '1'

        game_room = self.UNKNOWN
        if rule[0] == '0' and rule[2] == '0':
            game_room = self.IPPAN
        if rule[0] == '1' and rule[2] == '0':
            game_room = self.JOUKYUU
        if rule[0] == '0' and rule[2] == '1':
            game_room = self.TOKUJOU
        if rule[0] == '1' and rule[2] == '1':
            game_room = self.HOUHOU

        game_rule = self.UNKNOWN
        if is_hanchan:
            if is_fast:
                game_rule = self.HANCHAN_FAST_TANYAO_RED_FIVES
            else:
                if is_aka and is_open_tanyao:
                    game_rule = self.HANCHAN_TANYAO_RED_FIVES
                if not is_open_tanyao and not is_aka:
                    game_rule = self.HANCHAN_NO_TANYAO_NO_RED_FIVES
                if is_open_tanyao and not is_aka:
                    game_rule = self.HANCHAN_TANYAO_NO_RED_FIVES
        else:
            if is_fast:
                game_rule = self.TONPUSEN_FAST_TANYAO_RED_FIVES
            else:
                if is_aka and is_open_tanyao:
                    game_rule = self.TONPUSEN_TANYAO_RED_FIVES
                if not is_open_tanyao and not is_aka:
                    game_rule = self.TONPUSEN_NO_TANYAO_NO_RED_FIVES
                if is_open_tanyao and not is_aka:
                    game_rule = self.TONPUSEN_TANYAO_NO_RED_FIVES

        return lobby, game_rule, game_room

    def parse_names(self, tag):
        result = [
            unquote(self.get_attribute_content(tag, "n0")),
            unquote(self.get_attribute_content(tag, "n1")),
            unquote(self.get_attribute_content(tag, "n2")),
            unquote(self.get_attribute_content(tag, "n3"))
        ]

        # we are in hirosima game (for three players)
        if not result[-1]:
            del result[-1]

        return result

    def parse_rates(self, tag):
        result = self.get_attribute_content(tag, "rate").split(',')
        result = [float(i) for i in result]
        return result

    def parse_ranks(self, tag):
        result = self.get_attribute_content(tag, "dan").split(',')
        result = [float(i) for i in result]
        return result

    def parse_final_scores(self, tag):
        data = self.get_attribute_content(tag, 'owari')
        data = [float(i) for i in data.split(',')]

        # start at the beginning at take every second item (even)
        scores = data[::2]
        # start at second item and take every second item (odd)
        uma = data[1::2]

        return scores, uma

    def split_log_to_game_rounds(self, log_content: str):
        """
        XML parser was really slow here,
        so I built simple parser to separate log content on tags (grouped by rounds)
        """
        tag_start = 0
        rounds = []
        tag = None

        current_round_tags = []
        for x in range(0, len(log_content)):
            if log_content[x] == ">":
                tag = log_content[tag_start : x + 1]
                tag_start = x + 1

            # not useful tags
            skip_tags = ["SHUFFLE", "TAIKYOKU", "mjloggm"]
            if tag and any([x in tag for x in skip_tags]):
                tag = None

            # new hand was started
            if self.is_init_tag(tag) and current_round_tags:
                rounds.append(current_round_tags)
                current_round_tags = []

            # the end of the game
            if tag and "owari" in tag:
                rounds.append(current_round_tags)

            if tag:
                if self.is_init_tag(tag):
                    # we dont need seed information
                    # it appears in old logs format
                    find = re.compile(r'shuffle="[^"]*"')
                    tag = find.sub("", tag)

                # add processed tag to the round
                current_round_tags.append(tag)
                tag = None

        return rounds

    def get_attribute_content(self, tag: str, attribute_name: str):
        result = re.findall(r'{}="([^"]*)"'.format(attribute_name), tag)
        return result and result[0] or None

    def comma_separated_string_to_ints(self, string: str):
        return [int(x) for x in string.split(",")]

    def is_init_tag(self, tag):
        return tag and "INIT" in tag

    def is_agari_tag(self, tag):
        return tag and "AGARI" in tag

    def parse_meld(self, message):
        data = int(self.get_attribute_content(message, "m"))

        meld = Meld()
        meld.who = int(self.get_attribute_content(message, "who"))
        # 'from_who' is encoded relative the the 'who', so we want
        # to convert it to be relative to our player
        meld.from_who = ((data & 0x3) + meld.who) % 4

        if data & 0x4:
            self.parse_chi(data, meld)
        elif data & 0x18:
            self.parse_pon(data, meld)
        elif data & 0x20:
            self.parse_nuki(data, meld)
        else:
            self.parse_kan(data, meld)

        return meld

    def parse_chi(self, data, meld):
        meld.type = Meld.CHI
        t0, t1, t2 = (data >> 3) & 0x3, (data >> 5) & 0x3, (data >> 7) & 0x3
        base_and_called = data >> 10
        base = base_and_called // 3
        called = base_and_called % 3
        base = (base // 7) * 9 + base % 7
        meld.tiles = [t0 + 4 * (base + 0), t1 + 4 * (base + 1), t2 + 4 * (base + 2)]
        meld.called_tile = meld.tiles[called]

    def parse_pon(self, data, meld):
        t4 = (data >> 5) & 0x3
        t0, t1, t2 = ((1, 2, 3), (0, 2, 3), (0, 1, 3), (0, 1, 2))[t4]
        base_and_called = data >> 9
        base = base_and_called // 3
        called = base_and_called % 3
        if data & 0x8:
            meld.type = Meld.PON
            meld.tiles = [t0 + 4 * base, t1 + 4 * base, t2 + 4 * base]
            meld.called_tile = meld.tiles[called]
        else:
            meld.type = Meld.SHOUMINKAN
            meld.tiles = [t0 + 4 * base, t1 + 4 * base, t2 + 4 * base, t4 + 4 * base]
            meld.called_tile = meld.tiles[3]

    def parse_kan(self, data, meld):
        base_and_called = data >> 8
        base = base_and_called // 4
        meld.type = Meld.KAN
        meld.tiles = [4 * base, 1 + 4 * base, 2 + 4 * base, 3 + 4 * base]
        called = base_and_called % 4
        meld.called_tile = meld.tiles[called]
        # to mark closed\opened kans
        meld.opened = meld.who != meld.from_who

    def parse_nuki(self, data, meld):
        meld.type = Meld.NUKI
        meld.tiles = [data >> 8]

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

            if settings.IS_TEST_RUN:
                with open(log_file, 'wb') as f:
                    f.write(log_data)

        return log_data

    def _download_log(self, log_id):
        resp = urlopen('http://tenhou.net/0/log/?' + log_id)
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

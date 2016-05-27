import datetime

from django.test import TestCase
from django.utils import timezone

from tenhou_log_parser.constants import MahjongConstants
from tenhou_log_parser.main import TenhouLogParser


class TestCaseMixin(object):

    def _prepare_data(self, data):
        return data.replace('\n', '').replace('        ', '')


class ParseMetaInformationTestCase(TestCase, TestCaseMixin):

    def test_parse_final_scores(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <GO type="9" lobby="0"/>
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="%4E%6F%4E%61%6D%65%34" dan="2,3,10,1" rate="1564.57,1470.35,1238.80,1520.41" sx="M,M,M,M"/>
        <AGARI ba="1,3" hai="5,7,11,13,17,44,50,53,95,97,101" m="43019" machi="44" ten="30,3900,0" yaku="15,1,11,1,52,1" doraHai="9" who="0" fromWho="3" sc="310,72,362,0,104,0,194,-42" owari="382,49.0,362,16.0,104,-40.0,152,-25.0" />
        </mjloggm>
        """)

        results = TenhouLogParser().parse_log(log_data=data)
        self.assertEqual(len(results['players']), 4)

        self.assertEqual(results['players'][0]['seat'], 0)
        self.assertEqual(results['players'][0]['name'], 'NoName1')
        self.assertEqual(results['players'][0]['position'], 1)
        self.assertEqual(results['players'][0]['scores'], 38200)

        self.assertEqual(results['players'][1]['seat'], 1)
        self.assertEqual(results['players'][1]['name'], 'NoName2')
        self.assertEqual(results['players'][1]['position'], 2)
        self.assertEqual(results['players'][1]['scores'], 36200)

        self.assertEqual(results['players'][2]['seat'], 3)
        self.assertEqual(results['players'][2]['name'], 'NoName4')
        self.assertEqual(results['players'][2]['position'], 3)
        self.assertEqual(results['players'][2]['scores'], 15200)

        self.assertEqual(results['players'][3]['seat'], 2)
        self.assertEqual(results['players'][3]['name'], 'NoName3')
        self.assertEqual(results['players'][3]['position'], 4)
        self.assertEqual(results['players'][3]['scores'], 10400)

    def test_parse_players(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <GO type="9" lobby="0"/>
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="%4E%6F%4E%61%6D%65%34" dan="2,3,10,1" rate="1564.57,1470.35,1238.80,1520.41" sx="M,M,M,M"/>
        </mjloggm>
        """)

        results = TenhouLogParser().parse_log(log_data=data)
        self.assertEqual(results['game_type'], MahjongConstants.FOUR_PLAYERS)
        self.assertEqual(len(results['players']), 4)

        self.assertEqual(results['players'][0]['name'], 'NoName1')
        self.assertEqual(results['players'][1]['name'], 'NoName2')
        self.assertEqual(results['players'][2]['name'], 'NoName3')
        self.assertEqual(results['players'][3]['name'], 'NoName4')

    def test_parse_hirosima_players(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <GO type="9" lobby="0"/>
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="" dan="9,2,11,0" rate="1627.06,1479.85,1793.88,1500.00" sx="M,M,M,C"/>
        <UN n0="%4E%6F%4E%61%6D%65%31"/>
        </mjloggm>
        """)

        results = TenhouLogParser().parse_log(log_data=data)
        self.assertEqual(results['game_type'], MahjongConstants.THREE_PLAYERS)
        self.assertEqual(len(results['players']), 3)

        self.assertEqual(results['players'][0]['name'], 'NoName1')
        self.assertEqual(results['players'][1]['name'], 'NoName2')
        self.assertEqual(results['players'][2]['name'], 'NoName3')

    def test_parse_lobby(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <GO type="9" lobby="0"/>
        """)

        results = TenhouLogParser().parse_log(log_data=data)
        self.assertEqual(results['lobby'], 0)

        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <GO type="9" lobby="1111"/>
        """)

        results = TenhouLogParser().parse_log(log_data=data)
        self.assertEqual(results['lobby'], 1111)

    def test_parse_game_rule(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <GO type="9" lobby="0"/>
        """)

        results = TenhouLogParser().parse_log(log_data=data)
        self.assertEqual(results['lobby'], 0)

        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <GO type="9" lobby="1111"/>
        """)

        results = TenhouLogParser().parse_log(log_data=data)
        self.assertEqual(results['lobby'], 1111)

    def test_parse_game_type(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <GO type="9" lobby="0"/>
        """)
        results = TenhouLogParser().parse_log(log_data=data)
        self.assertEqual(results['game_rule'], MahjongConstants.HANCHAN_TANYAO_RED_FIVES)

        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <GO type="25" lobby="0"/>
        """)
        results = TenhouLogParser().parse_log(log_data=data)
        self.assertEqual(results['game_rule'], MahjongConstants.HANCHAN_TANYAO_RED_FIVES)

        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <GO type="1" lobby="0"/>
        """)
        results = TenhouLogParser().parse_log(log_data=data)
        self.assertEqual(results['game_rule'], MahjongConstants.TONPUSEN_TANYAO_RED_FIVES)

    def test_parse_game_date(self):
        results = TenhouLogParser().parse_log(log_id='2016051813gm-0001-0000-d455c767')
        self.assertEqual(results['game_date'], datetime.datetime(2016, 5, 18, 13, 0, tzinfo=timezone.utc))


class ParseRoundTestCase(TestCase, TestCaseMixin):

    def test_rounds_and_agari(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="%4E%6F%4E%61%6D%65%34" dan="2,3,10,1" rate="1564.57,1470.35,1238.80,1520.41" sx="M,M,M,M"/>
        <INIT/>
        <T76/><D123/><U125/>
        <AGARI who="0" fromWho="1" />
        <T76/><D123/><U125/>
        <INIT/>
        <T76/><D123/><U125/>
        <AGARI who="2" fromWho="1" owari="1,2,3,4,5,6,7,8"/>
        </mjloggm>
        """)

        results = TenhouLogParser().parse_log(log_data=data)

        for player in results['players']:
            self.assertEqual(len(player['rounds']), 2)

        player = next((i for i in results['players'] if i['seat'] == 0), None)
        self.assertEqual(player['rounds'][0]['is_win'], True)
        self.assertEqual(player['rounds'][0]['is_deal'], False)
        self.assertEqual(player['rounds'][0]['is_tsumo'], False)
        self.assertEqual(player['rounds'][0]['is_retake'], False)

        player = next((i for i in results['players'] if i['seat'] == 1), None)
        self.assertEqual(player['rounds'][0]['is_win'], False)
        self.assertEqual(player['rounds'][0]['is_deal'], True)
        self.assertEqual(player['rounds'][0]['is_tsumo'], False)
        self.assertEqual(player['rounds'][0]['is_retake'], False)

        player = next((i for i in results['players'] if i['seat'] == 2), None)
        self.assertEqual(player['rounds'][1]['is_win'], True)
        self.assertEqual(player['rounds'][1]['is_deal'], False)
        self.assertEqual(player['rounds'][1]['is_tsumo'], False)
        self.assertEqual(player['rounds'][1]['is_retake'], False)

        player = next((i for i in results['players'] if i['seat'] == 1), None)
        self.assertEqual(player['rounds'][1]['is_win'], False)
        self.assertEqual(player['rounds'][1]['is_deal'], True)
        self.assertEqual(player['rounds'][1]['is_tsumo'], False)
        self.assertEqual(player['rounds'][1]['is_retake'], False)

    def test_rounds_and_tsumo(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="%4E%6F%4E%61%6D%65%34" dan="2,3,10,1" rate="1564.57,1470.35,1238.80,1520.41" sx="M,M,M,M"/>
        <INIT/>
        <T76/><D123/><U125/>
        <AGARI who="0" fromWho="0" owari="1,2,3,4,5,6,7,8"/>
        </mjloggm>
        """)

        results = TenhouLogParser().parse_log(log_data=data)

        player = next((i for i in results['players'] if i['seat'] == 0), None)
        self.assertEqual(player['rounds'][0]['is_win'], True)
        self.assertEqual(player['rounds'][0]['is_deal'], False)
        self.assertEqual(player['rounds'][0]['is_tsumo'], True)
        self.assertEqual(player['rounds'][0]['is_retake'], False)

        player = next((i for i in results['players'] if i['seat'] == 1), None)
        self.assertEqual(player['rounds'][0]['is_deal'], False)

        player = next((i for i in results['players'] if i['seat'] == 2), None)
        self.assertEqual(player['rounds'][0]['is_deal'], False)

        player = next((i for i in results['players'] if i['seat'] == 3), None)
        self.assertEqual(player['rounds'][0]['is_deal'], False)

    def test_rounds_and_retake(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="%4E%6F%4E%61%6D%65%34" dan="2,3,10,1" rate="1564.57,1470.35,1238.80,1520.41" sx="M,M,M,M"/>
        <INIT/>
        <T76/><D123/><U125/>
        <AGARI who="0" fromWho="0" />
        <INIT/>
        <T76/><D123/><U125/>
        <RYUUKYOKU type="yao9" ba="0,0" sc="433,0,266,0,250,0,51,0" hai3="14,20,32,36,38,65,66,68,106,109,114,121,126,132" owari="1,2,3,4,5,6,7,8"/>
        </mjloggm>
        """)

        results = TenhouLogParser().parse_log(log_data=data)

        player = next((i for i in results['players'] if i['seat'] == 0), None)
        self.assertEqual(player['rounds'][1]['is_deal'], False)
        self.assertEqual(player['rounds'][1]['is_retake'], True)

        player = next((i for i in results['players'] if i['seat'] == 1), None)
        self.assertEqual(player['rounds'][1]['is_deal'], False)
        self.assertEqual(player['rounds'][1]['is_retake'], True)

        player = next((i for i in results['players'] if i['seat'] == 2), None)
        self.assertEqual(player['rounds'][1]['is_deal'], False)
        self.assertEqual(player['rounds'][1]['is_retake'], True)

        player = next((i for i in results['players'] if i['seat'] == 3), None)
        self.assertEqual(player['rounds'][1]['is_deal'], False)
        self.assertEqual(player['rounds'][1]['is_retake'], True)

    def test_rounds_and_double_ron(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="%4E%6F%4E%61%6D%65%34" dan="2,3,10,1" rate="1564.57,1470.35,1238.80,1520.41" sx="M,M,M,M"/>
        <INIT/>
        <T76/><D123/><U125/>
        <AGARI who="0" fromWho="2" />
        <AGARI who="1" fromWho="2" owari="1,2,3,4,5,6,7,8"/>
        </mjloggm>
        """)

        results = TenhouLogParser().parse_log(log_data=data)

        for player in results['players']:
            self.assertEqual(len(player['rounds']), 1)

        player = next((i for i in results['players'] if i['seat'] == 0), None)
        self.assertEqual(player['rounds'][0]['is_win'], True)
        self.assertEqual(player['rounds'][0]['is_deal'], False)

        player = next((i for i in results['players'] if i['seat'] == 1), None)
        self.assertEqual(player['rounds'][0]['is_win'], True)
        self.assertEqual(player['rounds'][0]['is_deal'], False)

        player = next((i for i in results['players'] if i['seat'] == 2), None)
        self.assertEqual(player['rounds'][0]['is_win'], False)
        self.assertEqual(player['rounds'][0]['is_deal'], True)

        player = next((i for i in results['players'] if i['seat'] == 3), None)
        self.assertEqual(player['rounds'][0]['is_win'], False)
        self.assertEqual(player['rounds'][0]['is_deal'], False)

    def test_rounds_and_open_hand(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="%4E%6F%4E%61%6D%65%34" dan="2,3,10,1" rate="1564.57,1470.35,1238.80,1520.41" sx="M,M,M,M"/>
        <INIT/>
        <T76/><D123/><U125/><N who="3" m="24815" />
        <AGARI who="0" fromWho="2" />
        <INIT/>
        <T76/><D123/><U125/><N who="2" m="6167" />
        <AGARI who="2" fromWho="1" owari="1,2,3,4,5,6,7,8"/>
        </mjloggm>
        """)

        results = TenhouLogParser().parse_log(log_data=data)

        for player in results['players']:
            self.assertEqual(len(player['rounds']), 2)

        player = next((i for i in results['players'] if i['seat'] == 0), None)
        self.assertEqual(player['rounds'][0]['is_open_hand'], False)
        self.assertEqual(player['rounds'][1]['is_open_hand'], False)

        player = next((i for i in results['players'] if i['seat'] == 1), None)
        self.assertEqual(player['rounds'][0]['is_open_hand'], False)
        self.assertEqual(player['rounds'][1]['is_open_hand'], False)

        player = next((i for i in results['players'] if i['seat'] == 2), None)
        self.assertEqual(player['rounds'][0]['is_open_hand'], False)
        self.assertEqual(player['rounds'][1]['is_open_hand'], True)

        player = next((i for i in results['players'] if i['seat'] == 3), None)
        self.assertEqual(player['rounds'][0]['is_open_hand'], True)
        self.assertEqual(player['rounds'][1]['is_open_hand'], False)

    def test_rounds_and_open_hand_and_closed_kan(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="%4E%6F%4E%61%6D%65%34" dan="2,3,10,1" rate="1564.57,1470.35,1238.80,1520.41" sx="M,M,M,M"/>
        <INIT/>
        <T76/><D123/><U125/><N who="0" m="33280" /><DORA hai="21" />
        <AGARI who="2" fromWho="1"/>
        <INIT/>
        <T76/><D123/><U125/><N who="1" m="33280" /><T76/><DORA hai="21" />
        <AGARI who="2" fromWho="1" owari="1,2,3,4,5,6,7,8"/>
        </mjloggm>
        """)

        results = TenhouLogParser().parse_log(log_data=data)

        player = next((i for i in results['players'] if i['seat'] == 0), None)
        self.assertEqual(player['rounds'][0]['is_open_hand'], False)
        self.assertEqual(player['rounds'][1]['is_open_hand'], False)

        player = next((i for i in results['players'] if i['seat'] == 1), None)
        self.assertEqual(player['rounds'][0]['is_open_hand'], False)
        self.assertEqual(player['rounds'][1]['is_open_hand'], True)

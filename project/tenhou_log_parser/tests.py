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

        self.assertEqual(results['players'][0]['seat'], 1)
        self.assertEqual(results['players'][0]['name'], 'NoName1')
        self.assertEqual(results['players'][0]['position'], 1)
        self.assertEqual(results['players'][0]['scores'], 38200)

        self.assertEqual(results['players'][1]['seat'], 2)
        self.assertEqual(results['players'][1]['name'], 'NoName2')
        self.assertEqual(results['players'][1]['position'], 2)
        self.assertEqual(results['players'][1]['scores'], 36200)

        self.assertEqual(results['players'][2]['seat'], 4)
        self.assertEqual(results['players'][2]['name'], 'NoName4')
        self.assertEqual(results['players'][2]['position'], 3)
        self.assertEqual(results['players'][2]['scores'], 15200)

        self.assertEqual(results['players'][3]['seat'], 3)
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

    def test_parse_rounds_and_agari(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="%4E%6F%4E%61%6D%65%34" dan="2,3,10,1" rate="1564.57,1470.35,1238.80,1520.41" sx="M,M,M,M"/>
        <INIT/>
        <AGARI who="0" fromWho="1" />
        <T76/><D123/><U125/>
        <INIT/>
        <AGARI who="2" fromWho="1" />
        </mjloggm>
        """)

        results = TenhouLogParser().parse_log(log_data=data)
        for player in results['players']:
            self.assertEqual(len(player['rounds']), 2)

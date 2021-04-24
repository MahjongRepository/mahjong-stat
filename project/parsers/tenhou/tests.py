import datetime
import unittest

from django.test import TestCase
from django.utils import timezone

from parsers.tenhou.constants import MahjongConstants
from parsers.tenhou.main import TenhouLogParser


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

        results = TenhouLogParser().parse_log('2016051813gm-0001-0000-d455c767', data)
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

    def test_parse_final_scores_and_end_of_the_round_with_retake(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <GO type="9" lobby="0"/>
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="%4E%6F%4E%61%6D%65%34" dan="2,3,10,1" rate="1564.57,1470.35,1238.80,1520.41" sx="M,M,M,M"/>
        <RYUUKYOKU ba="0,2" sc="214,-15,236,15,191,15,339,-15" hai1="13,19,22,50,52,54,57,62,97,100,104,128,131" hai2="5,7,9,11,12,15,45,46,58,59,93,94,102" owari="382,49.0,362,16.0,104,-40.0,152,-25.0" />
        </mjloggm>
        """)

        results = TenhouLogParser().parse_log('2016051813gm-0001-0000-d455c767', data)
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
        <RYUUKYOKU owari="0,0,0,0,0,0,0,0" />
        </mjloggm>
        """)

        results = TenhouLogParser().parse_log('2016051813gm-0001-0000-d455c767', data)
        self.assertEqual(results['game_type'], MahjongConstants.FOUR_PLAYERS)
        self.assertEqual(len(results['players']), 4)

        self.assertEqual(results['players'][0]['name'], 'NoName1')
        self.assertEqual(results['players'][1]['name'], 'NoName2')
        self.assertEqual(results['players'][2]['name'], 'NoName3')
        self.assertEqual(results['players'][3]['name'], 'NoName4')

        self.assertEqual(results['players'][0]['rate'], 1564.57)
        self.assertEqual(results['players'][1]['rate'], 1470.35)
        self.assertEqual(results['players'][2]['rate'], 1238.80)
        self.assertEqual(results['players'][3]['rate'], 1520.41)

        self.assertEqual(results['players'][0]['rank'], 2)
        self.assertEqual(results['players'][1]['rank'], 3)
        self.assertEqual(results['players'][2]['rank'], 10)
        self.assertEqual(results['players'][3]['rank'], 1)

    def test_parse_lobby(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <GO type="9" lobby="0"/>
        <RYUUKYOKU owari="0,0,0,0" />
        """)

        results = TenhouLogParser().parse_log('2016051813gm-0001-0000-d455c767', data)
        self.assertEqual(results['lobby'], 0)

        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <GO type="9" lobby="1111"/>
        <RYUUKYOKU owari="0,0,0,0" />
        """)

        results = TenhouLogParser().parse_log('2016051813gm-0001-0000-d455c767', data)
        self.assertEqual(results['lobby'], 1111)

    def test_parse_game_type(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <GO type="9" lobby="0"/>
        <RYUUKYOKU owari="0,0,0,0" />
        """)
        results = TenhouLogParser().parse_log('2016051813gm-0001-0000-d455c767', data)
        self.assertEqual(results['game_rule'], MahjongConstants.HANCHAN_TANYAO_RED_FIVES)

        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <GO type="25" lobby="0"/>
        <RYUUKYOKU owari="0,0,0,0" />
        """)
        results = TenhouLogParser().parse_log('2016051813gm-0001-0000-d455c767', data)
        self.assertEqual(results['game_rule'], MahjongConstants.HANCHAN_TANYAO_RED_FIVES)

        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <GO type="1" lobby="0"/>
        <RYUUKYOKU owari="0,0,0,0" />
        """)
        results = TenhouLogParser().parse_log('2016051813gm-0001-0000-d455c767', data)
        self.assertEqual(results['game_rule'], MahjongConstants.TONPUSEN_TANYAO_RED_FIVES)

    def test_parse_game_date(self):
        results = TenhouLogParser().parse_log(log_id='2016051813gm-0001-0000-d455c767')
        self.assertEqual(results['game_date'], datetime.datetime(2016, 5, 18, 13, 0, tzinfo=timezone.utc))


class ParseRoundTestCase(TestCase, TestCaseMixin):

    def test_rounds_and_agari(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="%4E%6F%4E%61%6D%65%34" dan="2,3,10,1" rate="1564.57,1470.35,1238.80,1520.41" sx="M,M,M,M"/>

        <INIT seed="1,0"/>
        <T76/><D123/><U125/>
        <AGARI who="0" fromWho="1" ten="2,4000,0"/>

        <INIT seed="1,0"/>
        <T76/><D123/><U125/>
        <AGARI who="2" fromWho="1" owari="1,2,3,4,5,6,7,8" ten="3,6000,0"/>

        </mjloggm>
        """)

        results = TenhouLogParser().parse_log('2016051813gm-0001-0000-d455c767', data)

        for player in results['players']:
            self.assertEqual(len(player['rounds']), 2)

        player = next((i for i in results['players'] if i['seat'] == 0), None)
        self.assertEqual(player['rounds'][0]['is_win'], True)
        self.assertEqual(player['rounds'][0]['win_scores'], 4000)
        self.assertEqual(player['rounds'][0]['lose_scores'], 0)
        self.assertEqual(player['rounds'][0]['is_deal'], False)
        self.assertEqual(player['rounds'][0]['is_tsumo'], False)
        self.assertEqual(player['rounds'][0]['is_retake'], False)

        player = next((i for i in results['players'] if i['seat'] == 1), None)
        self.assertEqual(player['rounds'][0]['win_scores'], 0)
        self.assertEqual(player['rounds'][0]['lose_scores'], 4000)
        self.assertEqual(player['rounds'][0]['is_win'], False)
        self.assertEqual(player['rounds'][0]['is_deal'], True)
        self.assertEqual(player['rounds'][0]['is_tsumo'], False)
        self.assertEqual(player['rounds'][0]['is_retake'], False)

        player = next((i for i in results['players'] if i['seat'] == 2), None)
        self.assertEqual(player['rounds'][1]['is_win'], True)
        self.assertEqual(player['rounds'][1]['win_scores'], 6000)
        self.assertEqual(player['rounds'][1]['lose_scores'], 0)
        self.assertEqual(player['rounds'][1]['is_deal'], False)
        self.assertEqual(player['rounds'][1]['is_tsumo'], False)
        self.assertEqual(player['rounds'][1]['is_retake'], False)

        player = next((i for i in results['players'] if i['seat'] == 1), None)
        self.assertEqual(player['rounds'][1]['win_scores'], 0)
        self.assertEqual(player['rounds'][1]['lose_scores'], 6000)
        self.assertEqual(player['rounds'][1]['is_win'], False)
        self.assertEqual(player['rounds'][1]['is_deal'], True)
        self.assertEqual(player['rounds'][1]['is_tsumo'], False)
        self.assertEqual(player['rounds'][1]['is_retake'], False)

    def test_rounds_and_tsumo(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="%4E%6F%4E%61%6D%65%34" dan="2,3,10,1" rate="1564.57,1470.35,1238.80,1520.41" sx="M,M,M,M"/>

        <INIT seed="1,0"/>
        <T76/><D123/><U125/>
        <AGARI who="0" fromWho="0" owari="1,2,3,4,5,6,7,8" ten="30,2000,0" sc="157,20,245,-5,376,-10,222,-5"/>

        </mjloggm>
        """)

        results = TenhouLogParser().parse_log('2016051813gm-0001-0000-d455c767', data)

        player = next((i for i in results['players'] if i['seat'] == 0), None)
        self.assertEqual(player['rounds'][0]['is_win'], True)
        self.assertEqual(player['rounds'][0]['win_scores'], 2000)
        self.assertEqual(player['rounds'][0]['is_deal'], False)
        self.assertEqual(player['rounds'][0]['is_tsumo'], True)
        self.assertEqual(player['rounds'][0]['is_retake'], False)

        player = next((i for i in results['players'] if i['seat'] == 1), None)
        self.assertEqual(player['rounds'][0]['is_deal'], False)
        self.assertEqual(player['rounds'][0]['lose_scores'], 500)

        player = next((i for i in results['players'] if i['seat'] == 2), None)
        self.assertEqual(player['rounds'][0]['is_deal'], False)
        self.assertEqual(player['rounds'][0]['lose_scores'], 1000)

        player = next((i for i in results['players'] if i['seat'] == 3), None)
        self.assertEqual(player['rounds'][0]['is_deal'], False)
        self.assertEqual(player['rounds'][0]['lose_scores'], 500)

    def test_rounds_and_retake(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="%4E%6F%4E%61%6D%65%34" dan="2,3,10,1" rate="1564.57,1470.35,1238.80,1520.41" sx="M,M,M,M"/>

        <INIT seed="1,0"/>
        <T76/><D123/><U125/>
        <AGARI who="0" fromWho="0" ten="0,1,2" />

        <INIT seed="1,0"/>
        <T76/><D123/><U125/>
        <RYUUKYOKU type="yao9" ba="0,0" sc="433,0,266,0,250,0,51,0" hai3="14,20,32,36,38,65,66,68,106,109,114,121,126,132" owari="1,2,3,4,5,6,7,8"/>

        </mjloggm>
        """)

        results = TenhouLogParser().parse_log('2016051813gm-0001-0000-d455c767', data)

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

        <INIT seed="1,0"/>
        <T76/><D123/><U125/>
        <AGARI who="0" fromWho="2" ten="2,2000,0"/>
        <AGARI who="1" fromWho="2" owari="1,2,3,4,5,6,7,8" ten="2,3000,0"/>

        </mjloggm>
        """)

        results = TenhouLogParser().parse_log('2016051813gm-0001-0000-d455c767', data)

        for player in results['players']:
            self.assertEqual(len(player['rounds']), 1)

        player = next((i for i in results['players'] if i['seat'] == 0), None)
        self.assertEqual(player['rounds'][0]['is_win'], True)
        self.assertEqual(player['rounds'][0]['win_scores'], 2000)
        self.assertEqual(player['rounds'][0]['lose_scores'], 0)
        self.assertEqual(player['rounds'][0]['is_deal'], False)

        player = next((i for i in results['players'] if i['seat'] == 1), None)
        self.assertEqual(player['rounds'][0]['is_win'], True)
        self.assertEqual(player['rounds'][0]['win_scores'], 3000)
        self.assertEqual(player['rounds'][0]['lose_scores'], 0)
        self.assertEqual(player['rounds'][0]['is_deal'], False)

        player = next((i for i in results['players'] if i['seat'] == 2), None)
        self.assertEqual(player['rounds'][0]['is_win'], False)
        self.assertEqual(player['rounds'][0]['is_deal'], True)
        self.assertEqual(player['rounds'][0]['lose_scores'], 5000)
        self.assertEqual(player['rounds'][0]['win_scores'], 0)

        player = next((i for i in results['players'] if i['seat'] == 3), None)
        self.assertEqual(player['rounds'][0]['is_win'], False)
        self.assertEqual(player['rounds'][0]['is_deal'], False)
        self.assertEqual(player['rounds'][0]['win_scores'], 0)
        self.assertEqual(player['rounds'][0]['lose_scores'], 0)

    def test_rounds_and_open_hand(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="%4E%6F%4E%61%6D%65%34" dan="2,3,10,1" rate="1564.57,1470.35,1238.80,1520.41" sx="M,M,M,M"/>

        <INIT seed="1,0"/>
        <T76/><D123/><U125/><N who="3" m="24815" />
        <AGARI who="0" fromWho="2" ten="0,1,2"/>

        <INIT seed="1,0"/>
        <T76/><D123/><U125/><N who="2" m="6167" />
        <AGARI who="2" fromWho="1" owari="1,2,3,4,5,6,7,8" ten="0,1,2"/>

        </mjloggm>
        """)

        results = TenhouLogParser().parse_log('2016051813gm-0001-0000-d455c767', data)

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

        <INIT seed="1,0"/>
        <T76/><D123/><U125/><N who="0" m="33280" /><DORA hai="21"/>
        <AGARI who="2" fromWho="1" ten="0,1,2"/>

        <INIT seed="1,0"/>
        <T76/><D123/><U125/><N who="1" m="51314" /><T76/><DORA hai="21"/>
        <AGARI who="2" fromWho="1" owari="1,2,3,4,5,6,7,8" ten="0,1,2"/>

        </mjloggm>
        """)

        results = TenhouLogParser().parse_log('2016051813gm-0001-0000-d455c767', data)

        player = next((i for i in results['players'] if i['seat'] == 0), None)
        self.assertEqual(player['rounds'][0]['is_open_hand'], False)
        self.assertEqual(player['rounds'][1]['is_open_hand'], False)

        player = next((i for i in results['players'] if i['seat'] == 1), None)
        self.assertEqual(player['rounds'][0]['is_open_hand'], False)
        self.assertEqual(player['rounds'][1]['is_open_hand'], True)

    def test_rounds_and_call_riichi(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="%4E%6F%4E%61%6D%65%34" dan="2,3,10,1" rate="1564.57,1470.35,1238.80,1520.41" sx="M,M,M,M"/>

        <INIT seed="1,0"/>
        <REACH who="0" step="1"/><D47/><REACH who="0" ten="255,216,261,258" step="2"/>
        <AGARI who="2" fromWho="1" ten="0,1,2"/>

        <INIT seed="1,0"/>
        <T76/><D123/><U125/><REACH who="0" step="1"/><D47/>
        <AGARI who="2" fromWho="1" owari="1,2,3,4,5,6,7,8" ten="0,1,2"/>

        </mjloggm>
        """)

        results = TenhouLogParser().parse_log('2016051813gm-0001-0000-d455c767', data)

        player = next((i for i in results['players'] if i['seat'] == 0), None)
        self.assertEqual(player['rounds'][0]['is_riichi'], True)
        self.assertEqual(player['rounds'][1]['is_riichi'], True)

        player = next((i for i in results['players'] if i['seat'] == 1), None)
        self.assertEqual(player['rounds'][0]['is_riichi'], False)
        self.assertEqual(player['rounds'][1]['is_riichi'], False)

        player = next((i for i in results['players'] if i['seat'] == 2), None)
        self.assertEqual(player['rounds'][0]['is_riichi'], False)
        self.assertEqual(player['rounds'][1]['is_riichi'], False)

        player = next((i for i in results['players'] if i['seat'] == 3), None)
        self.assertEqual(player['rounds'][0]['is_riichi'], False)
        self.assertEqual(player['rounds'][1]['is_riichi'], False)

    def test_rounds_and_damaten(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="%4E%6F%4E%61%6D%65%34" dan="2,3,10,1" rate="1564.57,1470.35,1238.80,1520.41" sx="M,M,M,M"/>

        <INIT seed="1,0"/>
        <AGARI who="0" fromWho="1" ten="0,1,2"/>

        <INIT seed="1,0"/>
        <T76/><D123/><U125/>
        <REACH who="0" step="1"/><D47/><REACH who="0" ten="255,216,261,258" step="2"/>
        <AGARI who="0" fromWho="1" ten="0,1,2"/>

        <INIT seed="1,0"/>
        <T76/><D123/><U125/><N who="0" m="6167" />
        <AGARI who="0" fromWho="1" owari="1,2,3,4,5,6,7,8" ten="0,1,2"/>

        </mjloggm>
        """)

        results = TenhouLogParser().parse_log('2016051813gm-0001-0000-d455c767', data)

        player = next((i for i in results['players'] if i['seat'] == 0), None)
        self.assertEqual(player['rounds'][0]['is_riichi'], False)
        self.assertEqual(player['rounds'][0]['is_win'], True)
        self.assertEqual(player['rounds'][0]['is_open_hand'], False)
        self.assertEqual(player['rounds'][0]['is_damaten'], True)

        # riichi is not damaten
        player = next((i for i in results['players'] if i['seat'] == 0), None)
        self.assertEqual(player['rounds'][1]['is_riichi'], True)
        self.assertEqual(player['rounds'][1]['is_win'], True)
        self.assertEqual(player['rounds'][1]['is_open_hand'], False)
        self.assertEqual(player['rounds'][1]['is_damaten'], False)

        # open hand is not damaten
        player = next((i for i in results['players'] if i['seat'] == 0), None)
        self.assertEqual(player['rounds'][2]['is_riichi'], False)
        self.assertEqual(player['rounds'][2]['is_win'], True)
        self.assertEqual(player['rounds'][2]['is_open_hand'], True)
        self.assertEqual(player['rounds'][2]['is_damaten'], False)

    def test_rounds_and_honba(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <UN n0="%4E%6F%4E%61%6D%65%31" n1="%4E%6F%4E%61%6D%65%32" n2="%4E%6F%4E%61%6D%65%33" n3="%4E%6F%4E%61%6D%65%34" dan="2,3,10,1" rate="1564.57,1470.35,1238.80,1520.41" sx="M,M,M,M"/>

        <INIT seed="0,0"/>
        <T76/><D123/><U125/>
        <AGARI who="0" fromWho="1" ten="0,1,2" />

        <INIT seed="0,1"/>
        <T76/><D123/><U125/>
        <AGARI who="0" fromWho="1" ten="0,1,2" />

        <INIT seed="1,0"/>
        <T76/><D123/><U125/>
        <AGARI who="2" fromWho="1" owari="1,2,3,4,5,6,7,8" ten="0,1,2"/>

        </mjloggm>
        """)

        results = TenhouLogParser().parse_log('2016051813gm-0001-0000-d455c767', data)

        player = next((i for i in results['players'] if i['seat'] == 0), None)
        self.assertEqual(player['rounds'][0]['round_number'], 0)
        self.assertEqual(player['rounds'][0]['honba'], 0)
        self.assertEqual(player['rounds'][1]['round_number'], 0)
        self.assertEqual(player['rounds'][1]['honba'], 1)
        self.assertEqual(player['rounds'][2]['round_number'], 1)
        self.assertEqual(player['rounds'][2]['honba'], 0)

    def test_fix_double_ron_wrong_parsing(self):
        data = self._prepare_data("""
        <mjloggm ver="2.3">
        <UN n0="%64%61%6B%65%31%6D%6A" n1="%68%75%73%6B%61%72" n2="%D0%B7%D0%B0%D1%87%D0%B5%D0%BC" n3="%E3%81%A1%E3%82%85%E3%82%93%E3%81%9F" dan="14,14,14,14" rate="1987.69,1871.62,1866.08,1920.37" sx="M,M,M,M"/>
        
        <INIT seed="6,0,0,0,2,14" ten="292,285,253,170" oya="2" hai0="80,114,117,16,130,25,42,71,54,97,27,119,32" hai1="33,15,41,38,46,31,78,83,82,96,52,51,7" hai2="4,72,93,131,66,61,109,26,53,57,18,17,73" hai3="35,107,100,24,81,84,34,56,40,90,79,118,43"/>
        <AGARI ba="0,1" hai="50,54,59,112,114" m="19471,14375,45067" machi="50" ten="30,3900,0" yaku="12,1,52,1,54,1" doraHai="14" who="0" fromWho="3" sc="292,49,285,0,243,0,170,-39" />
        <AGARI ba="0,0" hai="4,8,12,17,18,19,50,53,57,61,66,69,72,73" machi="50" ten="40,12000,1" yaku="1,1,52,3,53,0" doraHai="14" doraHaiUra="132" who="2" fromWho="3" sc="341,0,285,0,243,120,131,-120" owari="1,2,3,4,5,6,7,8" ten="0,1,2" />
        
        </mjloggm>
        """)

        results = TenhouLogParser().parse_log('2021030410gm-0029-0000-7530e444', data)

        player = next((i for i in results['players'] if i['seat'] == 0), None)
        self.assertEqual(player['rounds'][0]['han'], 3)
        self.assertEqual(player['rounds'][0]['fu'], 30)
        self.assertEqual(player['rounds'][0]['win_scores'], 4900)

        player = next((i for i in results['players'] if i['seat'] == 2), None)
        self.assertEqual(player['rounds'][0]['han'], 4)
        self.assertEqual(player['rounds'][0]['fu'], 40)
        self.assertEqual(player['rounds'][0]['win_scores'], 12000)

        player = next((i for i in results['players'] if i['seat'] == 3), None)
        self.assertEqual(player['rounds'][0]['is_win'], False)
        self.assertEqual(player['rounds'][0]['han'], 4)
        self.assertEqual(player['rounds'][0]['fu'], 40)
        self.assertEqual(player['rounds'][0]['lose_scores'], 12000)

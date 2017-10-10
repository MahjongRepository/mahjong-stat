class MahjongConstants(object):
    UNKNOWN = 0

    # game type
    FOUR_PLAYERS = 1
    THREE_PLAYERS = 2

    GAME_TYPES = [
        [UNKNOWN, 'Unknown'],
        [FOUR_PLAYERS, 'Standard game'],
        [THREE_PLAYERS, 'Hirosima'],
    ]

    # game rules
    TONPUSEN_NO_TANYAO_NO_RED_FIVES = 1
    TONPUSEN_TANYAO_NO_RED_FIVES = 2
    TONPUSEN_TANYAO_RED_FIVES = 3
    TONPUSEN_FAST_TANYAO_RED_FIVES = 4

    HANCHAN_NO_TANYAO_NO_RED_FIVES = 5
    HANCHAN_TANYAO_NO_RED_FIVES = 6
    HANCHAN_TANYAO_RED_FIVES = 7
    HANCHAN_FAST_TANYAO_RED_FIVES = 8

    GAME_RULES = [
        [UNKNOWN, 'Unknown'],
        [TONPUSEN_NO_TANYAO_NO_RED_FIVES, 'Tonpusen. No tanyao, no red fives'],
        [TONPUSEN_TANYAO_NO_RED_FIVES, 'Tonpusen. Tanyao, no red fives'],
        [TONPUSEN_TANYAO_RED_FIVES, 'Tonpusen. Tanyao, red fives'],
        [TONPUSEN_FAST_TANYAO_RED_FIVES, 'Tonpusen. Tanyao, red fives. Fast'],

        [HANCHAN_NO_TANYAO_NO_RED_FIVES, 'Hanchan. No tanyao, no red fives'],
        [HANCHAN_TANYAO_NO_RED_FIVES, 'Hanchan. Tanyao, no red fives'],
        [HANCHAN_TANYAO_RED_FIVES, 'Hanchan. Tanyao, red fives'],
        [HANCHAN_FAST_TANYAO_RED_FIVES, 'Hanchan. Tanyao, red fives. Fast'],
    ]

    NEWBIE = 0
    NINTH_KYU = 1
    EIGHTH_KYU = 2
    SEVENTH_KYU = 3
    SIXTH_KYU = 4
    FIFTH_KYU = 5
    FOURTH_KYU = 6
    THIRD_KYU = 7
    SECOND_KYU = 8
    FIRST_KYU = 9
    FIRST_DAN = 10
    SECOND_DAN = 11
    THIRD_DAN = 12
    FOURTH_DAN = 13
    FIFTH_DAN = 14
    SIXTH_DAN = 15
    SEVENTH_DAN = 16
    EIGHTH_DAN = 17
    NINTH_DAN = 18
    TENTH_DAN = 19
    TENHOU_DAN = 20

    RANKS = [
        [NEWBIE, u'新人'],
        [NINTH_KYU, u'9級'],
        [EIGHTH_KYU, u'8級'],
        [SEVENTH_KYU, u'7級'],
        [SIXTH_KYU, u'6級'],
        [FIFTH_KYU, u'5級'],
        [FOURTH_KYU, u'4級'],
        [THIRD_KYU, u'3級'],
        [SECOND_KYU, u'2級'],
        [FIRST_KYU, u'1級'],
        [FIRST_DAN, u'初段'],
        [SECOND_DAN, u'二段'],
        [THIRD_DAN, u'三段'],
        [FOURTH_DAN, u'四段'],
        [FIFTH_DAN, u'五段'],
        [SIXTH_DAN, u'六段'],
        [SEVENTH_DAN, u'七段'],
        [EIGHTH_DAN, u'八段'],
        [NINTH_DAN, u'九段'],
        [TENTH_DAN, u'十段'],
        [TENHOU_DAN, u'天鳳位'],
    ]

    # 門前清模和
    MENZEN_TSUMO = 0
    # 立直
    RIICHI = 1
    # 一発
    IPPATSU = 2
    # 槍槓
    CHANKAN = 3
    # 嶺上開花
    RINSHAN_KAIHOU = 4
    # 海底摸月
    HAITEI = 5
    # 河底撈魚
    HOUTEI = 6
    # 平和
    PINFU = 7
    # 断幺九
    TANYAO = 8
    # 一盃口
    IIPEIKO = 9
    # 自風 東
    YAKUHAI_SEAT_TON = 10
    # 自風 南
    YAKUHAI_SEAT_NAN = 11
    # 自風 西
    YAKUHAI_SEAT_XIA = 12
    # 自風 北
    YAKUHAI_SEAT_PEI = 13
    # 場風 東
    YAKUHAI_ROUND_TON = 14
    # 場風 南
    YAKUHAI_ROUND_NAN = 15
    # 場風 西
    YAKUHAI_ROUND_XIA = 16
    # 場風 北
    YAKUHAI_ROUND_PEI = 17
    # 役牌 白
    YAKUHAI_HAKU = 18
    # 役牌 發
    YAKUHAI_HATSU = 19
    # 役牌 中
    YAKUHAI_CHUN = 20
    # 両立直
    DABURU_RIICHI = 21
    # 七対子
    CHIITOITSU = 22
    # 混全帯幺九
    CHANTA = 23
    # 一気通貫
    ITTSU = 24
    # 三色同順
    SANSHOKU_DOUJUN = 25
    # 三色同刻
    SANSHOKU_DOUKOU = 26
    # 三槓子
    SANKANTSU = 27
    # 対々和
    TOITOI = 28
    # 三暗刻
    SANANKOU = 29
    # 小三元
    SHOUSANGEN = 30
    # 混老頭
    HONROUTOU = 31
    # 二盃口
    RYANPEIKOU = 32
    # 純全帯幺九
    JUNCHAN = 33
    # 混一色
    HONITSU = 34
    # 清一色
    CHINITSU = 35
    # 人和
    RENHOU = 36
    # 天和
    TENHOU = 37
    # 地和
    CHIHOU = 38
    # 大三元
    DAISANGEN = 39
    # 四暗刻
    SUUANKOU = 40
    # 四暗刻単騎
    SUUANKOU_TANKI = 41
    # 字一色
    TSUU_IISOU = 42
    # 緑一色
    RYUUIISOU = 43
    # 清老頭
    CHINROUTOU = 44
    # 九蓮宝燈
    CHUUREN_POUTO = 45
    # 純正九蓮宝燈
    CHUUREN_POUTO_9_WAIT = 46
    # 国士無双
    KOKUSHI_MUSOU = 47
    # 国士無双１３面
    KOKUSHI_MUSOU_13_WAIT = 48
    # 大四喜
    DAISUUSHI = 49
    # 小四喜
    SHOUSUUSHI = 50
    # 四槓子
    SUUKANTSU = 51
    # ドラ
    DORA = 52
    # 裏ドラ
    URADORA = 53
    # 赤ドラ
    AKADORA = 54

    # Aggregated yakuhai
    YAKUHAI = 100

    YAKUMAN = [
       [TENHOU, 'Tenhou'],
       [CHIHOU, 'Chiihou'],
       [DAISANGEN, 'Daisangen'],
       [SUUANKOU, 'Suuankou'],
       [SUUANKOU_TANKI, 'Suuankou taki'],
       [TSUU_IISOU, 'Tsuu iisou'],
       [RYUUIISOU, 'Ryuuiisou'],
       [CHINROUTOU, 'Chinroutou'],
       [CHUUREN_POUTO, 'Chuuren poutou'],
       [CHUUREN_POUTO_9_WAIT, 'Chuuren poutou (9 wait)'],
       [KOKUSHI_MUSOU, 'Kokushi musou'],
       [KOKUSHI_MUSOU_13_WAIT, 'Kokushi musou (13 wait)'],
       [DAISUUSHI, 'Daisuushii'],
       [SHOUSUUSHI, 'Shousuushii'],
       [SUUKANTSU, 'Suukantsu'],
    ]

    YAKU = [
        [MENZEN_TSUMO, 'Menzen tsumo'],
        [RIICHI, 'Riichi'],
        [IPPATSU, 'Ippatsu'],
        [CHANKAN, 'Chankan'],
        [RINSHAN_KAIHOU, 'Rinshan kaihou'],
        [HAITEI, 'Haitei'],
        [HOUTEI, 'Houtei'],
        [PINFU, 'Pinfu'],
        [TANYAO, 'Tanyao'],
        [IIPEIKO, 'Iipeikou'],
        [YAKUHAI, 'Yakuhai'],
        [DABURU_RIICHI, 'Daburu Riichi'],
        [CHIITOITSU, 'Chiitoitsu'],
        [CHANTA, 'Chanta'],
        [ITTSU, 'Ittsuu'],
        [SANSHOKU_DOUJUN, 'Sanshoku doujin'],
        [SANSHOKU_DOUKOU, 'Sanshoku doukou'],
        [SANKANTSU, 'Sankantsu'],
        [TOITOI, 'Toitoi'],
        [SANANKOU, 'Sanankou'],
        [SHOUSANGEN, 'Shou Sangen'],
        [HONROUTOU, 'Honroutou'],
        [RYANPEIKOU, 'Ryanpeikou'],
        [JUNCHAN, 'Junchan'],
        [HONITSU, 'Honitsu'],
        [CHINITSU, 'Chinitsu'],
        [RENHOU, 'Renhou'],
    ]

    DORAS = [
        [DORA, 'Dora'],
        [URADORA, 'Uradora'],
        [AKADORA, 'Akadora']
    ]

    ALL_YAKU = YAKU + YAKUMAN + DORAS

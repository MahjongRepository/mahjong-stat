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

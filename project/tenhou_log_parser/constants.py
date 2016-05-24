class MahjongConstants(object):
    UNKNOWN = 0

    # game type
    FOUR_PLAYERS = 1
    THREE_PLAYERS = 2

    GAME_TYPES = (
        (UNKNOWN, 'Unknown'),
        (FOUR_PLAYERS, 'Standard game'),
        (THREE_PLAYERS, 'Hirosima'),
    )

    # game rules
    TONPUSEN_NO_TANYAO_NO_RED_FIVES = 1
    TONPUSEN_TANYAO_NO_RED_FIVES = 2
    TONPUSEN_TANYAO_RED_FIVES = 3
    TONPUSEN_FAST_TANYAO_RED_FIVES = 4
    HANCHAN_NO_TANYAO_NO_RED_FIVES = 5
    HANCHAN_TANYAO_NO_RED_FIVES = 6
    HANCHAN_TANYAO_RED_FIVES = 7
    HANCHAN_FAST_TANYAO_RED_FIVES = 8

    GAME_RULES = (
        (TONPUSEN_NO_TANYAO_NO_RED_FIVES, 'Tonpusen. No tanyao, no red fives'),
        (TONPUSEN_TANYAO_NO_RED_FIVES, 'Tonpusen. Tanyao, no red fives'),
        (TONPUSEN_TANYAO_RED_FIVES, 'Tonpusen. Tanyao, red fives'),
        (TONPUSEN_FAST_TANYAO_RED_FIVES, 'Tonpusen. Tanyao, red fives. Fast'),

        (HANCHAN_NO_TANYAO_NO_RED_FIVES, 'Hanchan. No tanyao, no red fives'),
        (HANCHAN_TANYAO_NO_RED_FIVES, 'Hanchan. Tanyao, no red fives'),
        (HANCHAN_TANYAO_RED_FIVES, 'Hanchan. Tanyao, red fives'),
        (HANCHAN_FAST_TANYAO_RED_FIVES, 'Hanchan. Tanyao, red fives. Fast'),
    )

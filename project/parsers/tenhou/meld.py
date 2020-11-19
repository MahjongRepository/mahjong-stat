class Meld:
    CHI = "chi"
    PON = "pon"
    KAN = "kan"
    SHOUMINKAN = "shouminkan"
    NUKI = "nuki"

    who = None
    tiles = None
    type = None
    from_who = None
    called_tile = None
    # we need it to distinguish opened and closed kan
    opened = True

    def __init__(self, meld_type=None, tiles=None, opened=True, called_tile=None, who=None, from_who=None):
        self.type = meld_type
        self.tiles = tiles or []
        self.opened = opened
        self.called_tile = called_tile
        self.who = who
        self.from_who = from_who

    def __str__(self):
        return "Type: {}, Tiles: {}".format(self.type, self.tiles)

    # for calls in array
    def __repr__(self):
        return self.__str__()

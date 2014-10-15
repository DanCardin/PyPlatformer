from object import Object


class Wall(Object):
    def __init__(self, pos, typ, tile):
        Object.__init__(self, pos)
        self.type = typ  # 0 = empty, 1 = solid, 2 = start, 3 = end, 4 = deadly
        self.tile = tile

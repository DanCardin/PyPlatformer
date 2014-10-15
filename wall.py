from enum import Enum
from object import Object


class Tile(Enum):
    Empty = 0
    Solid = 1
    Start = 2
    End = 3
    Deadly = 4


class Wall(Object):
    def __init__(self, pos, type, tile):
        Object.__init__(self, pos)
        self.type = Tile(type)
        self.tile = tile

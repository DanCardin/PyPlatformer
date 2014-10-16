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
        self._type = Tile(type)
        self._tile = tile

    def getTile(self):
        return self._tile

    def getType(self):
        return self._type

    def setType(self, type):
        self._type = type

    def setTile(self, tile):
        self._tile = tile

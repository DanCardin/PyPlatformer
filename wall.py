from enum import Enum
from object import Object
from lib.events import EventStream


class Tiles(Enum):
    Empty = 0
    Solid = 1
    Start = 2
    End = 3
    Deadly = 4


class Wall(Object, EventStream):
    def __init__(self, pos, type, tile):
        Object.__init__(self, pos)
        EventStream.__init__(self)
        self._type = Tiles(type)
        self._tile = tile

    def getTile(self):
        return self._tile

    def getType(self):
        return self._type

    def setType(self, type):
        self._type = Tiles(type)
        self._notify()

    def setTile(self, tile):
        self._tile = tile
        self._notify()

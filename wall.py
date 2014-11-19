from enum import Enum
from object import Object


class Tiles(Enum):
    Empty = 0
    Solid = 1
    Start = 2
    End = 3
    Deadly = 4


class Wall(Object):
    def __init__(self, pos, type, tile):
        Object.__init__(self, pos)
        self._subs = []
        self._type = Tiles(type)
        self._tile = tile

    def _notify(self):
        for sub in self._subs:
            sub(self)

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

    def subscribe(self, sub):
        self._subs.append(sub)
        sub(self)

import const
from enum import Enum
from object import Object
from events import EventStream


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
        self.notify()

    def setTile(self, tile):
        self._tile = tile
        self.notify()

    @property
    def relX(self):
        return self.x % const.res

    @property
    def relY(self):
        return self.y % const.res

    @Object.x.setter
    def x(self, value):
        self._rect.x = value
        self.notify()

    @Object.y.setter
    def y(self, value):
        self._rect.y = value
        self.notify()

    @Object.w.setter
    def w(self, value):
        self._rect.w = value
        self.notify()

    @Object.h.setter
    def h(self, value):
        self._rect.h = value
        self.notify()

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
    EnemySpawn = 5


class Wall(Object, EventStream):
    def __init__(self, pos, type, tile, attribs={}):
        Object.__init__(self, pos)
        EventStream.__init__(self)
        self._lastType = None
        self._type = Tiles(type)
        self._tile = tile
        self._attribs = attribs
        self._mapX = self.x // const.res
        self._mapY = self.y // const.res

    def getAttr(self, key):
        return self._attribs.get(key, None)

    def setAttr(self, key, value):
        self._attribs[key] = value
        self.notify()

    def getTile(self):
        return self._tile

    def getType(self):
        return self._type

    def setType(self, type):
        self._lastType = self._type
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

    @property
    def mapX(self):
        return self._mapX

    @property
    def mapY(self):
        return self._mapY

    @Object.x.setter
    def x(self, value):
        absX = const.res * self.mapX
        relVal = min(absX + 31, max(absX, value))
        self._rect.x = relVal
        self.w = self.w

    @Object.y.setter
    def y(self, value):
        absY = const.res * self.mapY
        relVal = min(absY + 31, max(absY, value))
        self._rect.y = relVal
        self.h = self.h

    @Object.w.setter
    def w(self, value):
        self._rect.w = min(32 - self.relX, max(1, value - self.x))
        self.notify()

    @Object.h.setter
    def h(self, value):
        self._rect.h = min(32 - self.relY, max(1, value - self.y))
        self.notify()

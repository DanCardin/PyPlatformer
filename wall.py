import const
from enum import Enum
from object import Object
from events import EventStream


class Tiles(Enum):
    """
    The different types that a Tile can be.
    """
    Empty = 0
    Solid = 1
    Start = 2
    End = 3
    Deadly = 4
    EnemySpawn = 5


class Wall(Object, EventStream):
    """
    A Rectangular object that represents an in-game unit of the Map.
    """
    def __init__(self, rect, type, tile, attribs={}):
        """
        `rect` - The absolute position and size of the Wall in in-game units.
        `type` - The type of the Wall, in `Tiles`
        `tile` - The integer to indicate the tileset tile to use when displaying this object.
        `attribs` - A `Dict` containing any additional metadata to associate with the `Wall`.
        """
        super().__init__(rect=rect)
        self._lastType = None
        self._type = Tiles(type)
        self._tile = tile
        self._attribs = attribs
        self._mapX = self.x // const.res
        self._mapY = self.y // const.res

    def getAttr(self, key):
        """
        Returns the attribute associated with the key, `key`.
        Returns `None` if `key` does not exist.
        """
        return self._attribs.get(key, None)

    def setAttr(self, key, value):
        """
        Sets the attribute, `key` to `value`.
        """
        self._attribs[key] = value
        self.notify()

    def getTile(self):
        """
        Returns the tile of the `Wall`.
        """
        return self._tile

    def getType(self):
        """
        Returns the type of the `Wall`.
        """
        return self._type

    def setType(self, type):
        """
        Sets the type of the `Wall` to `type`.
        """
        self._lastType = self._type
        self._type = Tiles(type)
        self.notify()

    def setTile(self, tile):
        """
        Sets the tile of the `Wall` to `tile`.
        """
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

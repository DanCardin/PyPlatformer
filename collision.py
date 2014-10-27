from enum import Enum
from const import *
from wall import Tile


class Direction(Enum):
    Top = 1
    Bottom = 2
    Left = 3
    Right = 4


class Collision(object):
    def __init__(self, parent, level):
        self._parent = parent
        self._pRect = self._parent
        self._level = level

    def collDir(self, dx, dy, collideBox):
        result = None
        if self._pRect.colliderect(collideBox):
            if dx > 0:
                self._pRect.right = collideBox.left
                result = Direction.Right
            if dx < 0:
                self._pRect.left = collideBox.right
                result = Direction.Left
            if dy > 0:
                self._pRect.bottom = collideBox.top
                result = Direction.Bottom
            if dy < 0:
                self._pRect.top = collideBox.bottom
                result = Direction.Top

        return result

    def collideWalls(self, dx, dy):
        tx, ty = int(self._pRect.x / res), int(self._pRect.y / res)
        rects = [[tx, ty], [tx + 1, ty], [tx, ty + 1], [tx + 1, ty + 1]]

        result = None
        for x, y in rects:
            if self._level.map.get(x, y).getType() == Tile.Solid:
                result = self.collDir(dx, dy, self._level.map.get(x, y))
                if result:
                    return result

    def collideEntities(self, dx, dy):
        for i in range(self._level.entityId):
            obj = self._level.get(i)
            if self._parent != obj:
                if self._parent.inertia < obj.inertia:
                    if self.collDir(dx, dy, obj) == 3:
                        return obj
        return 0

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
        self.parent = parent
        self.pRect = self.parent
        self.level = level

    def collDir(self, dx, dy, collideBox):
        result = None
        if self.pRect.colliderect(collideBox):
            if dx > 0:
                self.pRect.right = collideBox.left
                result = Direction.Right
            if dx < 0:
                self.pRect.left = collideBox.right
                result = Direction.Left
            if dy > 0:
                self.pRect.bottom = collideBox.top
                result = Direction.Bottom
            if dy < 0:
                self.pRect.top = collideBox.bottom
                result = Direction.Top

        return result

    def collideWalls(self, dx, dy):
        tx, ty = int(self.pRect.x / res), int(self.pRect.y / res)
        rects = [[tx, ty], [tx + 1, ty], [tx, ty + 1], [tx + 1, ty + 1]]

        result = None
        for x, y in rects:
            if self.level.map.get(x, y).getType() == Tile.Solid:
                result = self.collDir(dx, dy, self.level.map.get(x, y))
                if result:
                    return result

    def collideEntities(self, dx, dy):
        for i in range(self.level.entityId):
            obj = self.level.get(i)
            if self.parent != obj:
                if self.parent.inertia < obj.inertia:
                    if self.collDir(dx, dy, obj) == 3:
                        return obj
        return 0

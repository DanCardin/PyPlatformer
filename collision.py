import const
from enum import Enum
from wall import Tiles


class Direction(Enum):
    Top = 1
    Bottom = 2
    Left = 3
    Right = 4


class Collision(object):
    def __init__(self, parent, level, solidCollision=True):
        self._parent = parent
        self._pRect = self._parent
        self._level = level
        self._solidCollision = solidCollision

    def solidCollision(self, direc, collideBox):
        if direc is Direction.Right:
            self._pRect.right = collideBox.left
        if direc is Direction.Left:
            self._pRect.left = collideBox.right
        if direc is Direction.Bottom:
            self._pRect.bottom = collideBox.top
        if direc is Direction.Top:
            self._pRect.top = collideBox.bottom

    def getColDir(self, dx, dy, collideBox):
        if self._pRect.colliderect(collideBox):
            if dx > 0:
                return Direction.Right
            if dx < 0:
                return Direction.Left
            if dy > 0:
                return Direction.Bottom
            if dy < 0:
                return Direction.Top

    def getCollisionTiles(self):
        tx, ty = self._pRect.x // const.res, self._pRect.y // const.res
        result = set()
        for x, y in [(tx, ty), (tx + 1, ty), (tx, ty + 1), (tx + 1, ty + 1)]:
            if self._level.map.inRange(x, y) == (x, y):
                result.add((x, y))
        return result

    def collideWalls(self, dx, dy):
        result = {}
        for x, y in self.getCollisionTiles():
            tile = self._level.map.get(x, y)
            colDir = self.getColDir(dx, dy, tile)
            if colDir:
                ttype = tile.getType()
                if self._solidCollision and ttype == Tiles.Solid:
                    self.solidCollision(colDir, tile)
                if ttype != Tiles.Empty:
                    result.setdefault(ttype, set()).add(colDir)

        return result

    def ceaseColliding(self):
        tEnts = self._level._entity_map.get(self._parent.getId())
        if tEnts:
            for tile in tEnts:
                self._level._position_map.get(tile).remove(self._parent)
            self._level._entity_map.pop(self._parent.getId())

    def startColliding(self):
        self._level._entity_map[self._parent.getId()] = self.getCollisionTiles()
        for i in self._level._entity_map[self._parent.getId()]:
            self._level._position_map[i].append(self._parent)

    def __call__(self, dx, dy):
        self.ceaseColliding()
        self.startColliding()

        result = self.collideWalls(dx, dy)
        result.update(self.collideEntities(dx, dy))
        return result

    def collideEntities(self, dx, dy):
        result = {}
        for tile in self.getCollisionTiles():
            for obj in self._level._position_map[tile]:
                if self._parent is not obj:
                    colDir = self.getColDir(dx, dy, obj)
                    if colDir:
                        result.setdefault(obj.getAltName() or obj.getId(), set()).add(colDir)
                        try:
                            if self._solidCollision and obj.collision._solidCollision:
                                self.solidCollision(colDir, obj)
                        except AttributeError:
                            pass
        return result

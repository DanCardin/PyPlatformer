import const
from enum import Enum
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
        return set([(tx, ty), (tx + 1, ty), (tx, ty + 1), (tx + 1, ty + 1)])

    def collideWalls(self, dx, dy):
        result = {}
        for x, y in self.getCollisionTiles():
            tile = self._level.map.get(x, y)
            colDir = self.getColDir(dx, dy, tile)
            if colDir:
                ttype = tile.getType()
                if ttype == Tile.Solid:
                    self.solidCollision(colDir, tile)
                if ttype != Tile.Empty:
                    result.setdefault(ttype, set()).add(colDir)

        return result

    def __call__(self, dx, dy):
        ents = self._level._entity_map
        poss = self._level._position_map

        if not ents.get(self._parent.getId()):
            ents[self._parent.getId()] = self.getCollisionTiles()

        for i in ents[self._parent.getId()]:
            poss2 = poss.get(i)
            if i in poss2:
                poss2.remove(i)

        result = self.collideWalls(dx, dy)

        ents[self._parent.getId()] = self.getCollisionTiles()
        for i in ents[self._parent.getId()]:
            poss[i].append(self._parent)

        result.update(self.collideEntities(dx, dy))
        return result

    def collideEntities(self, dx, dy):
        result = {}
        for tile in self.getCollisionTiles():
            for obj in self._level._position_map[tile]:
                if self._parent is not obj:
                    colDir = self.getColDir(dx, dy, obj)
                    result.setdefault(obj.getId(), set()).add(colDir)
                    self.solidCollision(colDir, obj)
        return result
    # def collideEntities(self, dx, dy):
    #     for i in range(self._level.entityId):
    #         obj = self._level.get(i)
    #         if self._parent != obj:
    #             if self._parent.inertia < obj.inertia:
    #                 if self.getColDir(dx, dy, obj) == 3:
    #                     return obj
    #     return 0

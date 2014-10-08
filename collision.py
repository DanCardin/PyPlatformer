from const import *


class Top:
    pass


class Bottom:
    pass


class Left:
    pass


class Right:
    pass


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
                result = Right
            if dx < 0:
                self.pRect.left = collideBox.right
                result = Left
            if dy > 0:
                self.pRect.bottom = collideBox.top
                result = Bottom
            if dy < 0:
                self.pRect.top = collideBox.bottom
                result = Top

        return result

    def collideWalls(self, dx, dy):
        tx, ty = int(self.pRect.x / res), int(self.pRect.y / res)
        rects = [[tx, ty], [tx + 1, ty], [tx, ty + 1], [tx + 1, ty + 1]]

        result = None
        for h in rects:
            if self.level.map.getType(int(h[0]), int(h[1])) == 1:
                wam = self.level.map.wallDim(int(h[0]), int(h[1]))
                result = self.collDir(dx, dy, wam)
                if result:
                    return result
        # return result

    def collideEntities(self, dx, dy):
        for i in range(self.level.entityId):
            obj = self.level.get(i)
            if self.parent != obj:
                if self.parent.inertia < obj.inertia:
                    if self.collDir(dx, dy, obj) == 3:
                        return obj
        return 0

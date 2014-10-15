class Move(object):
    def __init__(self, pRect, speed, collision=None):
        self.pRect = pRect
        self.collision = collision
        self._topSpeed = speed
        self._speed = [0, 0]

    def _incrSpeed(self, backing, x=None, y=None):
        if x is not None:
            backing[0] += x
        if y is not None:
            backing[1] += y

    def _setSpeed(self, backing, x=None, y=None):
        if x is not None:
            backing[0] = x
        if y is not None:
            backing[1] = y

    def _getSpeed(self, backing, x=None, y=None):
        if x and y:
            return (backing[0], backing[1])
        if x:
            return backing[0]
        if y:
            return backing[1]

        raise Exception("Either x, y, or both should be True")

    def setSpeed(self, x=None, y=None):
        self._setSpeed(self._speed, x, y)

    def incrSpeed(self, x=None, y=None):
        self._incrSpeed(self._speed, x, y)

    def getSpeed(self, x=None, y=None):
        return self._getSpeed(self._speed, x, y)

    def getTopSpeed(self, x=None, y=None):
        return self._getSpeed(self._topSpeed, x, y)

    def moveSingleAxis(self, dx, dy):
        self.pRect.x += dx
        self.pRect.y += dy
        if self.collision:
            return self.collision.collideWalls(dx, dy)

    def move(self):
        result = []
        if self._speed[0] != 0:
            self._speed[0] = min(self._topSpeed[0], self._speed[0])

            xresult = self.moveSingleAxis(self._speed[0], 0)
            result.append(xresult if xresult is not None else [])
        if self._speed[1] != 0:
            self._speed[1] = min(self._topSpeed[1], self._speed[1])

            yresult = self.moveSingleAxis(0, self._speed[1])
            result.append(yresult if yresult is not None else [])
        return result
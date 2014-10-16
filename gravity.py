from collision import Direction


class Gravity(object):
    def __init__(self, parent, value):
        self._parent = parent
        self._mag = abs(value)
        self._value = value

    def getDir(self):
        return (self._value > 0) - (0 - self._value)

    def positiveDir(self):
        return self.getDir() > 0

    def getMag(self):
        return self._mag

    def setMag(self, mag):
        self._mag = mag

    def _applyGravity(self):
        self._parent.move.incrSpeed(y=self._value)

    def _resetFromCollision(self, collisions):
        self._parent.move.setSpeed(y=0)

    def tick(self, collisions):
        direction = Direction.Bottom if self.positiveDir() else Direction.Top
        if not direction in collisions:
            self._applyGravity()

        if [i for i in [Direction.Bottom, Direction.Top] if i in collisions]:
            self._resetFromCollision(collisions)


class GravityLine(Gravity):
    def __init__(self, parent, mag, h=None, v=None):
        if h and v:
            raise Exception("Gravity can either be horizontal or vertical.")

        super().__init__(parent, mag)

        self.h = h
        self.v = v

        self._crossedLine = False
        """True while parent has crossed the gravity line, but not yet landed on ground."""

    def _resetFromCollision(self, collisions):
        super()._resetFromCollision(collisions)

        self._crossedLine = False

    def tick(self, collision):
        super().tick(collision)

        if self.h:
            oldValue = self._value
            lower = self._parent.y > self.h
            self._value = -self._mag if lower else self._mag
            if oldValue != self._value:
                self._crossedLine = True

from collision import Direction
from wall import Tiles


class Jumping(object):
    def __init__(self, parent, gravity, jumps):
        self.parent = parent
        self.gravity = gravity
        self.jumping = False
        self.curJump = 0
        self.maxJump = jumps
        self.muted = False

    def muteJump(self):
        self.muted = True

    def jump(self):
        if not self.jumping:
            self.muted = False
            self.jumping = True
            self.curJump -= 1
            topSpeed = self.parent.getTopSpeed(y=True)
            jumpSpeed = -topSpeed if self.gravity.positiveDir() else topSpeed
            self.parent.setSpeed(y=jumpSpeed)

    def tick(self, collisions):
        self._ignore = [Tiles.Empty, Tiles.Start, Tiles.End, Tiles.Deadly]
        collisions = {c for a, b in collisions.items() for c in b if a not in self._ignore}
        direction = Direction.Bottom if self.gravity.positiveDir() else Direction.Top
        if direction in collisions:
            self.curJump = self.maxJump

        if self.jumping:
            if self.muted:
                self.parent.incrSpeed(y=2 if self.gravity.positiveDir() else -2)
            if self.parent.getSpeed(y=True) * self.gravity.getDir() > 0:
                if (self.curJump > 0):
                    self.jumping = False

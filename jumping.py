from collision import Top, Bottom


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
        direction = Bottom if self.gravity.positiveDir() else Top
        if direction in collisions:
            self.curJump = self.maxJump

        if self.jumping:
            if self.muted:
                pass# self.parent.incrSpeed(y=2)
            if self.parent.getSpeed(y=True) * self.gravity.getDir() > 0:
                if (self.curJump > 0):
                    self.jumping = False

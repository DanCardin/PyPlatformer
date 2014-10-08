from object import *
from move import *
from collision import *
from display import *
from gravity import *
from jumping import *
from input import *
from const import res, screenSize


class MChar(Object):
    def __init__(self, size, speed, tileset, control, level):
        Object.__init__(self, size)
        self.collision = Collision(self, level)
        self.move = Move(self, speed, collision=self.collision)
        self.display = Display(tileset, self, size, True, True, 11)
        self.gravity = GravityLine(self, level.map.res, h=res * screenSize[1] / 2)
        self.jumping = Jumping(self.move, self.gravity, 2)
        self.input = Input()
        self.controlled = control

        if self.controlled:
            self.applyInputSettings()

        self.inertia = 1
        self.dir = 1

    def applyInputSettings(self):
        self.input.set(pygame.KEYDOWN, pygame.K_a, "left", self.startMove, "left")
        self.input.set(pygame.KEYDOWN, pygame.K_d, "right", self.startMove, "right")
        self.input.set(pygame.KEYDOWN, pygame.K_w, "up", self.startMove, "up")
        self.input.set(pygame.KEYDOWN, pygame.K_s, "down", self.startMove, "down")

        self.input.set(pygame.KEYUP, pygame.K_a, "left", self.stopMove, "left")
        self.input.set(pygame.KEYUP, pygame.K_d, "right", self.stopMove, "right")
        self.input.set(pygame.KEYUP, pygame.K_w, "up", self.stopMove, "up")
        self.input.set(pygame.KEYUP, pygame.K_s, "down", self.stopMove, "down")

    def startMove(self, arg):
        if arg == "left":
            self.move.setSpeed(x=-self.move.getTopSpeed(x=True))
        if arg == "right":
            self.move.setSpeed(x=self.move.getTopSpeed(x=True))
        if arg == "up":
            self.jumping.jump()

    def stopMove(self, arg):
        xspeed = self.move.getSpeed(x=True)
        if arg == "left" and xspeed < 0:
            self.move.setSpeed(x=0)
        if arg == "right" and xspeed > 0:
            self.move.setSpeed(x=0)
        if arg == "up":
            self.jumping.muteJump()

    def tick(self, inputs):
        self.input(inputs)
        self.dir = 1 if self.move.getSpeed(x=True) > 0 else -1

        collisions = self.move.move()
        self.jumping.tick(collisions)
        self.gravity.tick(collisions)

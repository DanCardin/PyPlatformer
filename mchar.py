import pygame
import const
from collision import Collision
from display import Display
from files import Files
from gravity import GravityLine
from input import Input
from jumping import Jumping
from object import Object
from move import Move
from wall import Tile
from weapons import NewWeapon
from ids import Id


class Dir(object):
    def __init__(self, rule, default=1):
        self._rule = rule
        self._dir = 1

    def getDir(self):
        return self._dir

    def tick(self):
        curDir = self._rule()
        if curDir:
            self._dir = curDir


class MChar(Object, Dir, Id):
    def __init__(self, start, size, speed, tileset, control, level):
        Object.__init__(self, (start[0], start[1], size[0], size[1]))
        Id.__init__(self)
        self.collision = Collision(self, level)
        self.move = Move(self, speed, collision=self.collision)
        self.display = Display(Files().loadImage(tileset), self, True, 11)
        self.gravity = GravityLine(self, 2, h=const.res * const.screenSize[1] / 2)
        self.jumping = Jumping(self.move, self.gravity, 2)
        self.input = Input()
        self.applyInputSettings()

        def _getDir():
            return self.move.getDir(x=True)
        Dir.__init__(self, _getDir)

        self._weapon = NewWeapon(self, (0, 0), level)

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

    def draw(self, surface, camera):
        self.display.draw(surface, camera)

    def tick(self, inputs):
        super().tick()
        self.input(inputs)
        self._weapon.tick(inputs)

        collisions = self.move()
        self.jumping.tick(collisions.get(Tile.Solid, []))
        self.gravity.tick(collisions.get(Tile.Solid, []))
        return collisions

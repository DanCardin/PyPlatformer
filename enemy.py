from object import *
from move import *
from collision import *
from display import *
from gravity import *
from jumping import *
from ai import *


class AI(object):
    def tick(self):
        pass


class Enemy(Object, Id, AI):
    def __init__(self, size, speed, tileset, level):
        Object.__init__(self, size)
        Id.__init__(self, altname="enemy")
        self.move = Move(speed, self)
        self.collision = Collision(self, level, "enemy")
        self.display = Display(tileset, self, True, (True, 11))
        self.gravity = Gravity(self.level.map.res, self.move, self)
        self.ai = AI("goomba", self, level)
        self.inertia = 1
        self.dead = False
        self.move.speed[0] = self.move.topSpeed[0]

    def tick(self):
        super().tick()


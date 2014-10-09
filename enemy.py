from object import *
from move import *
from collision import *
from display import *
from gravity import *
from jumping import *
from ai import *


class Enemy(Object):
    def __init__(self, Size, Speed, Tileset, Level):
        Object.__init__(self, Size)
        self.level = Level
        self.move = Move(Speed, self)
        self.collision = Collision(self, Level, "enemy")
        self.display = Display(Tileset, self, Size, True, (True, 11))
        self.gravity = Gravity(self.level.map.res, self.move, self)
        self.ai = AI("goomba", self, Level)
        self.inertia = 1
        self.dead = False
        self.move.speed[0] = self.move.topSpeed[0]

    def tick(self):
        self.ai.tick()


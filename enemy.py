import const
from object import Object
from move import Move
from collision import Collision
from display import Display
from gravity import GravityLine
from jumping import Jumping
from ids import Id
from files import Files
from wall import Tile


class AI(object):
    def tick(self):
        pass


class Enemy(Object, Id, AI):
    def __init__(self, size, speed, tileset, level):
        Object.__init__(self, size)
        Id.__init__(self, altname="enemy")
        self.collision = Collision(self, level, "enemy")
        self.move = Move(self, speed, self.collision)
        self.display = Display(Files().loadImage(tileset), self, True, 11)
        self.gravity = GravityLine(self, 2, h=const.res * const.screenSize[1] / 2)
        # self.ai = AI("goomba", self, level)
        self._alive = True
        self.move.setSpeed(x=self.move.getTopSpeed(x=True))

    def tick(self):
        super().tick()
        collisions = self.move()
        self.gravity.tick(collisions.get(Tile.Solid, []))
        if collisions.get("bullet"):
            self._alive = False


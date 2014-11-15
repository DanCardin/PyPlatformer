import const
from char import Health, Alive, Dir
from collision import Collision, Direction
from display import Display
from files import Files
from gravity import GravityLine
from ids import Id
from jumping import Jumping
from move import Move
from object import Object
from particle import Emitter, Behaviors
from wall import Tile


class EnemyEmitter(Emitter):
    def __init__(self, anchor, offset, level, maxEmitted=0):
        super().__init__(anchor, offset, maxEmitted)
        self._level = level
        self._part = None

    def _emit(self):
        if len(self._children) < self._maxEmitted:
            pos = Object(self._anchor.x + self._offset.x, self._anchor.y + self._offset.y, 20, 26)
            _part = Enemy(pos, (3, 16), const.playerTileset, self._level, 3)
            self._children.append(_part)


class AI(object):
    def tick(self, collisions):
        solid = collisions.get(Tile.Solid)
        if solid:
            if Direction.Left in solid and Direction.Bottom in solid:
                self._dir = 1
            if Direction.Right in solid and Direction.Bottom in solid:
                self._dir = -1
            self.move.setSpeed(x= self._dir * self.move.getTopSpeed(x=True))

        if collisions.get("bullet"):
            self.decHealth(1)
            self.move.setSpeed(y=-8)

        if self.getHealth() == 0:
            self.kill()


class Enemy(Object, Id, AI, Alive, Health):
    def __init__(self, size, speed, tileset, level, maxHealth):
        Object.__init__(self, size)
        Id.__init__(self, altname="enemy")
        Alive.__init__(self)
        Health.__init__(self, maxHealth)

        self.collision = Collision(self, level, "enemy")
        self.move = Move(self, speed, self.collision)
        self.display = Display(Files().loadImage(tileset), self, True, 11)
        self.gravity = GravityLine(self, 2, h=const.res * const.screenSize[1] / 2)
        self._dir = 1

    def tick(self):
        collisions = self.move()
        self.gravity.tick(collisions.get(Tile.Solid, []))
        super().tick(collisions)

    @Behaviors.cleanupCollision
    def kill(self):
        super().kill()

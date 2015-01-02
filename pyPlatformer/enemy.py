import const
from animation import Animation
from char import Health, Alive
from collision import Collision
from direction import Direction, Dir
from display import Display, Drawable
from files import Files
from gravity import GravityLine
from ids import IDed
from input import Inputable
from move import Move
from object import Object
from particle import MinTimeEmitter, Behaviors
from wall import Tiles


class EnemySpawn(MinTimeEmitter, Inputable):
    def __init__(self, level, **kwargs):
        super().__init__(**kwargs)
        self._level = level
        self._part = None

    def _emit(self):
        if len(self._children) < self._maxEmitted:
            x, y = self._offsetFunc()
            rect = (self._anchor.x + x, self._anchor.y + y, 20, 26)
            _part = Enemy(rect, (3, 16), const.playerTileset, self._level, 3)
            self._children.append(_part)


class AI(object):
    def __init__(self, klass):
        self._klass = klass
        self._dir = 1

    def tick(self, collisions):
        solid = collisions.get(Tiles.Solid)
        if solid:
            if Direction.Left in solid and Direction.Bottom in solid:
                self._dir = 1
            if Direction.Right in solid and Direction.Bottom in solid:
                self._dir = -1
            self._klass.move.setSpeed(x=self._dir * self._klass.move.getTopSpeed(x=True))


class Enemy(Object, Dir, IDed, Alive, Health, Drawable, Inputable):
    def __init__(self, rect, speed, tileset, level, maxHealth, **kwargs):
        super().__init__(rect=rect,
                         dirRule=lambda: {
                            -1: Direction.Left,
                            0: None,
                            1: Direction.Right,
                         }[self.move.getDir(x=True)],
                         idName="enemy",
                         baseHealth=maxHealth, **kwargs)

        self.collision = Collision(self, level, "enemy")
        self.move = Move(self, speed, self.collision)
        self.gravity = GravityLine(self, 2, h=level.map.h // 2)
        self._ai = AI(self)

        def _isMoving():
            return self.move.getSpeed(x=True) != 0

        def _hDir():
            return self.move.getDir(x=True)

        def _vDir():
            return {False: -1, True: 1}[self.gravity.positiveDir()]

        image = Files.loadImage(tileset)
        self._display = Display(image, self, Animation(image, 11, _isMoving, _hDir, _vDir), True)

    def tick(self):
        collisions = self.move()
        self.gravity.tick(collisions)
        self._ai.tick(collisions)

        if collisions.get("bullet"):
            self.decHealth(1)
            self.move.setSpeed(y=self.gravity.getDir() * -8)

        if self.getHealth() == 0:
            self.kill()

        return collisions

    @Behaviors.cleanupCollision
    def kill(self):
        super().kill()

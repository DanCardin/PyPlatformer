import const
from animation import Animation
from char import Health, Alive, Dir
from collision import Collision, Direction
from display import Display, Drawable
from files import Files
from gravity import GravityLine
from ids import Id
from move import Move
from object import Object
from particle import MinTimeEmitter, Behaviors
from wall import Tiles


class EnemyEmitter(MinTimeEmitter):
    def __init__(self, anchor, offset, level, maxEmitted=0, timeBetween=0):
        super().__init__(anchor, offset, maxEmitted, timeBetween)
        self._level = level
        self._part = None

    def _emit(self):
        if len(self._children) < self._maxEmitted:
            pos = Object(self._anchor.x + self._offset.x, self._anchor.y + self._offset.y, 20, 26)
            _part = Enemy(pos, (3, 16), const.playerTileset, self._level, 3)
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
            self._klass.move.setSpeed(x= self._dir * self._klass.move.getTopSpeed(x=True))


class Enemy(Object, Dir, Id, Alive, Health, Drawable):
    def __init__(self, size, speed, tileset, level, maxHealth):
        Object.__init__(self, size)
        Dir.__init__(self, lambda: self.move.getDir(x=True))
        Id.__init__(self, altname="enemy")
        Alive.__init__(self)
        Health.__init__(self, maxHealth)

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
        self._display = Display(image, self, True, Animation(image, 11, _isMoving, _hDir, _vDir))

    def tick(self):
        collisions = self.move()
        self.gravity.tick(collisions)
        self._ai.tick(collisions)

        if collisions.get("bullet"):
            self.decHealth(1)
            self.move.setSpeed(y=-8)

        if self.getHealth() == 0:
            self.kill()


    @Behaviors.cleanupCollision
    def kill(self):
        super().kill()

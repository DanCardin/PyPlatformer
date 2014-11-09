from char import Alive
from collision import Collision
from display import Display
from move import Move
from ids import Id
from object import Object


class Behaviors(object):
    def killAt(dx, dy):
        def _killAt(particle):
            try:
                particle._KA_dx += particle.move.getSpeed(x=True)
                particle._KA_dy += particle.move.getSpeed(y=True)
            except AttributeError:
                particle._KA_dx = 0
                particle._KA_dy = 0

            if (particle._KA_dx < -dx or particle._KA_dx > dx or
                    particle._KA_dy < -dy or particle._KA_dy > dy):
                particle.kill()
        return _killAt

    def killWhen(time=50):
        def _killWhen(particle):
            try:
                particle._KW_iterations += 1
            except AttributeError:
                particle._KW_iterations = 1

            if particle._KW_iterations > time:
                particle.kill()
        return _killWhen

    def moveAt(sx, sy):
        def _moveAt(particle):
            particle.move.setSpeed(sx, sy)
        return _moveAt

    def killOnCollision(exceptions):
        def _killOnCollisions(particle):
            try:
                if particle._KOC_kill:
                    particle.kill()
            except AttributeError:
                particle._KOC_kill = False

            for col in particle.getCollisions():
                if col not in exceptions:
                    particle._KOC_kill = True
                    break
        return _killOnCollisions

    def cleanupCollision(func=None):
        def _cleanupCollision(particle):
            if func is not None:
                func(particle)
            if not particle.isAlive():
                particle.collision.ceaseColliding()
        return _cleanupCollision


class Particle(Object, Id, Alive):
    def __init__(self, size, topSpeed, tileset, collide, *strategies, altname=None):
        Object.__init__(self, size)
        Id.__init__(self, altname)
        Alive.__init__(self)

        self.display = Display(tileset, self)
        if collide:
            self.collision = Collision(self, collide, False)
        self.move = Move(self, topSpeed, self.collision)
        self._strategies = strategies

    def getCollisions(self):
        return self._collisions

    def tick(self):
        self._collisions = self.move()
        for s in self._strategies:
            s(self)


class Emitter(object):
    def __init__(self, anchor, offset, maxEmitted=0):
        self._anchor = anchor
        self._offset = offset
        self._children = []
        self._maxEmitted = maxEmitted

    def _emit(self):
        raise NotImplementedError("Subclasses should implement this method")

    def getChildren(self):
        return self._children[:]

    def draw(self, surface, camera):
        for p in self._children:
            p.display.draw(surface, camera)

    def tick(self):
        self._emit()
        for p in self._children[:]:
            p.tick()
            if not p.isAlive():
                self._children.remove(p)

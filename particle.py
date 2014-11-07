from object import Object
from move import Move
from collision import Collision
from display import Display
from ids import Id


class Behaviors(object):
    def kill_at(dx, dy):
        def _kill_at(particle):
            try:
                particle._KA_dx += particle._move.getSpeed(x=True)
                particle._KA_dy += particle._move.getSpeed(y=True)
            except AttributeError:
                particle._KA_dx = 0
                particle._KA_dy = 0

            if (particle._KA_dx < -dx or particle._KA_dx > dx or
                    particle._KA_dy < -dy or particle._KA_dy > dy):
                particle.kill()
        return _kill_at

    def kill_when(time=50):
        def _kill_when(particle):
            try:
                particle._KW_iterations += 1
            except AttributeError:
                particle._KW_iterations = 1

            if particle._KW_iterations > time:
                particle.kill()
        return _kill_when

    def move_at(sx, sy):
        def _move_at(particle):
            particle._move.setSpeed(sx, sy)
        return _move_at

    def onDeathCollisionDestroy():
        def _onDeathCollisionDestroy(particle):
            if not particle._alive:
                particle.collision.ceaseColliding()
                particle.collision._level._entity_map.pop(particle.getId())
        return _onDeathCollisionDestroy

class Particle(Object, Id):
    def __init__(self, size, topSpeed, tileset, collide, *strategies, altname=None):
        Object.__init__(self, size)
        Id.__init__(self, altname)

        self.display = Display(tileset, self)
        if collide:
            self.collision = Collision(self, collide, False)
        self._move = Move(self, topSpeed, self.collision)
        self._alive = True
        self._strategies = strategies

    def kill(self):
        self._alive = False

    def isAlive(self):
        return self._alive

    def tick(self):
        for s in self._strategies:
            self._move()
            s(self)


class ParticleEmitter(object):
    def __init__(self, anchor, offset):
        self._anchor = anchor
        self._offset = offset
        self._particles = []
        self._config = None

    def _emit(self):
        raise NotImplementedError("Subclasses should implement this method")

    def setParticleConfig(self, *args):
        self._config = args

    def draw(self, surface, camera):
        for p in self._particles:
            p.display.draw(surface, camera)

    def tick(self):
        self._emit()
        for p in self._particles[:]:
            p.tick()
            if not p.isAlive():
                self._particles.remove(p)

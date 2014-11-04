from object import Object
from move import Move
from collision import Collision
from display import Display


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


class Particle(Object):
    def __init__(self, size, topSpeed, tileset, collide, *strategies):
        Object.__init__(self, size)

        self.display = Display(tileset, self)
        self._move = Move(self, topSpeed, collide)
        self._alive = True
        self._strategies = strategies

    def kill(self):
        self._alive = False

    def isAlive(self):
        return self._alive

    def tick(self):
        for s in self._strategies:
            s(self)
            self._move()


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

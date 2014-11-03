from object import Object
from move import Move
from collision import Collision
from display import Display
import itertools


class Behaviors(object):
    @classmethod
    def kill_at(dx, dy):
        def _kill_at(particle):
            particle._dx, particle._dy = particle.move.getSpeed(x=True, y=True)
            if (particle._dx < -max_x or particle._dx > max_x or
               particle._dy < -max_y or particle._dy > max_y):
                particle.kill()
        return _kill_at

    @classmethod
    def move_at(sx, sy):
        def _move_at(particle):
            particle.setSpeed(sx, sy)


class Particle(Object):
    def __init__(self, size, topSpeed, tileset, collide, *strategies):
        Object.__init__(self, size)

        self.move = Move(self, topSpeed, collide)
        self.display = Display(tileset, self)
        self._alive = True
        self._strategies = strategies

    def kill(self):
        self._alive = False

    def isAlive(self):
        return self._alive

    def tick(self):
        for s in self._strategies:
            s(self)


class ParticleEmitter(object):
    def __init__(self, anchor, offset):
        self._anchor = anchor
        self._offset = offset
        self._particles = []
        self._config = None

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

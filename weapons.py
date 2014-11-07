import pygame
from collision import Collision
from input import Input
from object import Object
from particle import Particle, ParticleEmitter, Behaviors


class NewWeapon(ParticleEmitter):
    def __init__(self, anchor, offset, level):
        super().__init__(anchor, offset)

        self._level = level
        self._part = None
        self._s = pygame.surface.Surface((20, 10))
        self._s.fill((255, 0, 0))

        self._input = Input()
        self._input.set(pygame.KEYDOWN, pygame.K_f, "fire", self.setNew)

    def setNew(self):
        pos = Object(self._anchor.x + self._offset[0], self._anchor.y + self._offset[1], 20, 10)
        self._part = Particle(pos,
                              (10, 0), self._s,
                              self._level,
                              Behaviors.kill_at(50, 50),
                              Behaviors.move_at(self._anchor.getDir() * 10, 0),
                              Behaviors.onDeathCollisionDestroy(),
                              altname="bullet")

    def _emit(self):
        if self._part:
            self._particles.append(self._part)
            self._part = None

    def tick(self, inputs):
        self._input(inputs)
        super().tick()

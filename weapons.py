import pygame
from input import Input, Inputable
from particle import Particle, Emitter, Behaviors
from surface import Surface


class Weapon(Emitter, Inputable):
    def __init__(self, level, **kwargs):
        super().__init__(**kwargs)

        self._level = level
        self._part = None
        self._s = Surface((20, 10))
        self._s.fill((255, 0, 0))

        self._input = Input(inputStream=self.getInputStream())
        self._input.set(pygame.KEYDOWN, self.createNew, pygame.K_f)

    def createNew(self):
        x, y = self._offsetFunc()
        self._part = Particle((self._anchor.x + x, self._anchor.y + y, 20, 10),
                              (10, 0),
                              self._s,
                              self._level,
                              Behaviors.killAt(150, 150),
                              Behaviors.moveAt(self._anchor.getIntDir() * 10, 0),
                              Behaviors.killOnCollision(exceptions=(self._anchor.getId(),)),
                              Behaviors.cleanupCollision(),
                              altname="bullet")
        if x < 0:
            self._part.x -= self._part.w
        self._part.move.setSpeed(x=self._part.move.getTopSpeed(x=True))

    def _emit(self):
        if self._part:
            self._children.append(self._part)
            self._part = None

    def tick(self):
        self._input()
        super().tick()

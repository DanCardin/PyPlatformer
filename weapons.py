import pygame
from collision import Collision
from enemy import Enemy
from input import Input
from object import Object
from particle import Particle, Emitter, Behaviors
from wall import Tile


class Weapon(Emitter):
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
                              (10, 0),
                              self._s,
                              self._level,
                              Behaviors.killAt(150, 150),
                              Behaviors.moveAt(self._anchor.getDir() * 10, 0),
                              Behaviors.killOnCollision(exceptions=(self._anchor.getId(),)),
                              Behaviors.cleanupCollision(),
                              altname="bullet")
        self._part.move.setSpeed(x=self._part.move.getTopSpeed(x=True))

    def _emit(self):
        if self._part:
            self._children.append(self._part)
            self._part = None

    def tick(self, inputs):
        self._input(inputs)
        super().tick()

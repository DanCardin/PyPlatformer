import pygame
import const
from math import ceil
from char import Health
from display import Display, Drawable
from files import Files
from object import Object


class HealthBar(Object, Drawable):
    def __init__(self, x, y, parent):
        Object.__init__(self, x, y, 0, 0)
        assert isinstance(parent, Health)

        self._hearts = []
        self._parent = parent

        hearts = Files.loadImage(const.heartsImg)
        self._heartFilled = (hearts.subsurface(Object(0, 0, 10, 16)),
                             hearts.subsurface(Object(10, 0, 10, 16)))
        self._heartEmpty = (hearts.subsurface(Object(20, 0, 10, 16)),
                            hearts.subsurface(Object(30, 0, 10, 16)))

        self._display = Display(klass=self)
        self.update()

    def update(self):
        self._heartLen = self._parent.getBaseHealth()
        self.w, self.h = 10 * self._heartLen + 2 * ceil(self._heartLen / 2), 16

        surf = pygame.surface.Surface((self.w, self.h))
        trans = self._heartFilled[0].get_at((0, 0))
        surf.fill(trans)
        surf.set_colorkey(trans)
        self._display.replace(surf)

        for i in range(self._heartLen):
            self._hearts.append(surf.subsurface(Object(10 * i + 2 * (i // 2), 0, 10, 16)))

        self._parent.subscribe("healthbar", self.recalculate)

    def recalculate(self, parent):
        health = self._parent.getHealth()
        for i in range(self._heartLen):
            ind = i % 2
            heartType = self._heartFilled if (i + 1) <= health else self._heartEmpty
            self._hearts[i].blit(heartType[ind], (0, 0))

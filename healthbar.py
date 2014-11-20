import pygame
from math import ceil
from char import Health
from display import Display, Drawable
from files import Files
from object import Object


class HealthBar(Object, Drawable):
    def __init__(self, x, y, parent):
        assert isinstance(parent, Health)

        self._hearts = []
        self._parent = parent
        self._heartWidth = int(ceil(self._parent.getBaseHealth() / 2))
        Object.__init__(self, 22 * self._heartWidth, 16)

        hearts = Files.loadImage("hearts.png")
        self._heartAmounts = (hearts.subsurface(Object(0, 0, 19, 16)),
                              hearts.subsurface(Object(19, 0, 19, 16)),
                              hearts.subsurface(Object(38, 0, 19, 16)))

        self._display = Display(None, self)
        self.update()

    def update(self):
        surf = pygame.surface.Surface((self.w, self.h))
        trans = self._heartAmounts[0].get_at((0, 0))
        surf.fill(trans)
        surf.set_colorkey(trans)

        maxHealth = self._parent.getBaseHealth()
        for i in range(self._heartWidth):
            self._hearts.append(surf.subsurface(Object(22 * i, 0, 19, 16)))
            if i <= maxHealth - 1:
                self._hearts[i].blit(self._heartAmounts[0], (0, 0))
            else:
                self._hearts[i].blit(self._heartAmounts[1], (0, 0))
        self._display.replace(surf)

import pygame
# from math import floor
from object import Object


class Animation(object):
    def __init__(self, klass, image, tLength):
        self._klass = klass
        self._tLength = tLength
        self._anim = {-1: {0: [], -1: []}, 1: {0: [], 1: []}}

        ix = image.get_width() / tLength
        iy = image.get_height()

        self._lastDir = 1

        self._anim[1][0].append(image.subsurface(Object((0, 0, ix, iy))))
        self._anim[-1][0].append(pygame.transform.flip(self._anim[1][0][0], True, False))
        for i in range(1, self._tLength):
            for e in range(2):
                self._anim[1][1].append(image.subsurface(Object((ix * i, 0, ix, iy))))
                self._anim[-1][-1].append(pygame.transform.flip(self._anim[1][1][-1], True, False))

    def animate(self, direction):
        if direction:
            self._lastDir = direction
        img = self._anim[self._lastDir][direction][0]
        self._anim[self._lastDir][direction] = self._anim[self._lastDir][direction][1:] + [img]
        self._klass.replace(img)

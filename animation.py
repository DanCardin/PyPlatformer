import pygame
# from math import floor
from object import Object


class Animation(object):
    def __init__(self, klass, image, tLength):
        self._klass = klass
        self._tLength = tLength
        self._anim = {-1: {0: [], -1: []}, 1: {0: [], 1: []}}
        self._currAnim = [0, 0, 0]
        self._preAnim = [0, 0]

        ix = image.get_width() / self._tLength
        iy = image.get_height()
        self._lastDir = 1
        self._index = 0

        self._anim[1][0].append(image.subsurface(Object((ix, iy))))
        self._anim[-1][0].append(pygame.transform.flip(self._anim[1][0][0], True, False))
        for i in range(1, self._tLength):
            self._anim[1][1].append(image.subsurface(Object((ix * i, 0, ix, iy))))
            self._anim[-1][-1].append(pygame.transform.flip(self._anim[1][1][i - 1], True, False))

    def animate(self, direction):
        # dir = direction * .5
        # if hasattr(self._klass, "move"):
        #     self._preAnim[0], self._preAnim[1] = self._currAnim[0], self._currAnim[1]
        #     self._currAnim[0] = {True: 1, False: 0}[self._klass.move.getSpeed(x=True) != 0]
        #     if self._currAnim[0] != 0:
        #         self._currAnim[1] = {True: 0, False: 1}[self._klass.move.getSpeed(x=True) > 0]
        #     else:
        #         self._currAnim[1] = self._preAnim[1]
        #     if [self._currAnim[0], self._currAnim[1]] != self._preAnim:
        #         self._currAnim[2] = 0
        #     if dir > 0:
        #         if self._currAnim[2] == len(self._anim[self._currAnim[0]][int(floor(self._currAnim[1]))]) - dir:
        #             self._currAnim[2] = 0
        #         else:
        #             self._currAnim[2] += dir
        #     else:
        #         if self._currAnim[2] <= 0:
        #             self._currAnim[2] = len(self._anim[self._currAnim[0]][int(floor(self._currAnim[1]))]) - dir
        #         else:
        #             self._currAnim[2] += dir
        #     ar = self._anim[self._currAnim[0]][self._currAnim[1]][int(floor(self._currAnim[2]))]
        # else:
        #     ar = self._anim[0][0][int(floor(self._currAnim + dir))]
        img = self._anim[self._lastDir][direction][0]
        self._anim[self._lastDir][direction][1:-1]
        # self._index = (self._index + 1) % (self._tLength - 1)
        if direction:
            self._lastDir = direction
        self._klass.display.replace(img)

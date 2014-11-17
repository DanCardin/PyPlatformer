import pygame
# from math import floor
from object import Object


class Animation(object):
    def __init__(self, image, tLength, actioning, hFlip=None, vFlip=None):
        self._image = image
        self._tLength = tLength
        self._actioning = actioning
        self._hFlip = hFlip
        self._vFlip = vFlip

        self._anim = {
            -1: {  # Negative Horizontal
                -1: {  # Negative Vertical
                    False: [],
                    True: []
                },
                1: {  # Postive Vertical
                    False: [],
                    True: []
                }
            },
            1: {  # Positive Horizontal
                -1: {  # Negative Vertical
                    False: [],
                    True: []
                },
                1: {  # Postive Vertical
                    False: [],
                    True: []
                }
            }
        }

        self._lastHDir = 1
        self._lastVDir = 1

    def build(self):
        ix = self._image.get_width() / self._tLength
        iy = self._image.get_height()

        self._anim[1][1][False].append(self._image.subsurface(Object((0, 0, ix, iy))))
        top = self._anim[1][1][False][-1]
        self._anim[-1][1][False].append(pygame.transform.flip(top, True, False))
        self._anim[1][-1][False].append(pygame.transform.flip(top, False, True))
        self._anim[-1][-1][False].append(pygame.transform.flip(top, True, True))

        for i in range(1, self._tLength):
            for e in range(2):
                self._anim[1][1][True].append(self._image.subsurface(Object((ix * i, 0, ix, iy))))
                top = self._anim[1][1][True][-1]
                if self._hFlip:
                    self._anim[-1][1][True].append(pygame.transform.flip(top, True, False))
                if self._vFlip:
                    self._anim[1][-1][True].append(pygame.transform.flip(top, False, True))
                if self._hFlip and self._vFlip:
                    self._anim[-1][-1][True].append(pygame.transform.flip(top, True, True))

    def animate(self):
        hDir = self._hFlip() if self._hFlip else None
        if hDir:
            self._lastHDir = hDir
        vDir = self._vFlip() if self._vFlip else None
        if vDir:
            self._lastVDir = vDir

        images = self._anim[self._lastHDir][self._lastVDir][self._actioning()]
        image = images[0]
        self._anim[self._lastHDir][self._lastVDir][self._actioning()] = images[1:] + [image]
        return image

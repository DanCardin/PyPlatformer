import pygame
from math import floor

class Animation(object):
    def __init__(self, Image, TLength, klass):
        self.klass = klass
        self.tLength = TLength
        self.anim = (([], []), ([], [])) #0: rest animation, 1: horiz animation,
        self.currAnim = [0, 0, 0]
        self.preAnim = [0, 0]
        tan = Image
        tx, ty = tan.get_width() / self.tLength, tan.get_height()

        for i in range(self.tLength):
            #ta = pygame.surface.Surface((tan.get_width(), tan.get_height()))
            ta = pygame.surface.Surface((20, tan.get_height()))
            ta.blit(tan, (-i * tx, 0, i * tx + tx, ty))
            if i == 0:
                self.anim[0][0].append(ta)
                self.anim[0][1].append(pygame.transform.flip(ta, 1, 0))
            else:
                self.anim[1][0].append(ta)
        for i in range(len(self.anim[1][0])):
            self.anim[1][1].append(pygame.transform.flip(self.anim[1][0][i], 1, 0))

    def animate(self, direction):
        dir = direction * .5
        if hasattr(self.klass, "move"):
            self.preAnim[0], self.preAnim[1] = self.currAnim[0], self.currAnim[1]
            self.currAnim[0] = {True: 1, False: 0}[self.klass.move.getSpeed(x=True) != 0]
            if self.currAnim[0] != 0:
                self.currAnim[1] = {True: 0, False: 1}[self.klass.move.getSpeed(x=True) > 0]
            else:
                self.currAnim[1] = self.preAnim[1]
            if [self.currAnim[0], self.currAnim[1]] != self.preAnim:
                self.currAnim[2] = 0
            if dir > 0:
                if self.currAnim[2] == len(self.anim[self.currAnim[0]][int(floor(self.currAnim[1]))]) - dir:
                    self.currAnim[2] = 0
                else:
                    self.currAnim[2] += dir
            else:
                if self.currAnim[2] <= 0:
                    self.currAnim[2] = len(self.anim[self.currAnim[0]][int(floor(self.currAnim[1]))]) - dir
                else:
                    self.currAnim[2] += dir
            ar = self.anim[self.currAnim[0]][self.currAnim[1]][int(floor(self.currAnim[2]))]
        else:
            ar = self.anim[0][0][int(floor(self.currAnim + dir))]
        self.klass.display.image = ar

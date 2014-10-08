import pygame

from object import *
from display import *


class Menu(object):
    def __init__(self, Pos, Showing):
        self.pos = Pos
        self.items = []
        self.enabled = Showing

    def append(self, item):
        self.items.append(item)

    def tick(self, input, mPos):
        t = []
        for i in self.items:
            tmp = len(t)
            if len(input) > 0:
                for event, key in input:
                    eTick = i.tick(event, self.pos, mPos)
                    if eTick is not None:
                        t.append(eTick)
            if len(t) > tmp:
                for e in self.items:
                    if e.toggle:
                        if e.tGroup == i.tGroup:
                            e.togState = {True: 1, False: 0}[e.togState == 2]
            i.tick(0, self.pos, mPos)
        return t

    def addItem(self, **kwargs):
        self.append(menuItem(**kwargs))

    def draw(self, surface):
        for i in self.items:
            i.display.draw(surface, Object((self.pos[0] * -1, self.pos[1] * -1, 0, 0)))


class menuItem(Object):
    def __init__(self, rect=(0, 0, 0, 0), rColor=(255, 255, 255), oColor=(0, 0, 0), text="",
                 tColor=(0, 0, 0), action=None, image = False, toggle = False, tGroup = None):
        Object.__init__(self, rect)
        self.action = action
        self.images = [pygame.surface.Surface((self.w, self.h)), pygame.surface.Surface((self.w, self.h))]
        self.tGroup = tGroup
        self.toggle = toggle
        if self.toggle:
            self.togState = 0

        colors = [rColor, oColor]
        for i in range(len(colors)):
            self.images[i].fill(colors[i])
            if text:
                txtImg = pygame.font.Font(None, 25).render(text, 1, tColor)
                self.images[i].blit(txtImg, ((self.images[i].get_width() / 2) - (txtImg.get_width() / 2), (self.images[i].get_height() / 2) - (txtImg.get_height() / 2)))
            if image is not False:
                self.images[i].blit(image, (1, 1))
        self.display = Display(self.images[0], self, self.images[0].get_rect, False)

    def move(self, vect):
        self[0] += self.vect[0]
        self[1] += self.vect[1]

    def tick(self, input, menu, mPos):
        collide = pygame.Rect(menu[0] + self.x, menu[1] + self.y, self.w, self.h).collidepoint(mPos[0], mPos[1])
        self.display.image = self.images[collide]
        if self.toggle:
            if self.togState:
                self.display.image = self.images[1]
        if input == pygame.MOUSEBUTTONDOWN:
            if collide:
                if self.toggle:
                    self.togState = 2
                if self.action:
                    return self.action

import pygame

from object import *
from display import *


class Menu(object):
    def __init__(self, surface, pos, enabled):
        self._surface = surface
        self.pos = pos
        self.items = {}
        self.enabled = enabled

    def select(self, key):
        return self.items.get(key)

    def tick(self, input, mPos):
        t = []
        if self.enabled:
            for item in self.items.values():
                tmp = len(t)
                if len(input) > 0:
                    for event, key in input:
                        eTick = item.tick(event, self.pos, mPos)
                        if eTick is not None:
                            t.append(eTick)
                if len(t) > tmp:
                    for e in self.items.values():
                        if e.toggle:
                            if e.tGroup == item.tGroup:
                                e.togState = {True: 1, False: 0}[e.togState == 2]
                item.tick(0, self.pos, mPos)
        return t

    def addItem(self, key, **kwargs):
        self.items[key] = MenuItem(action=key, **kwargs)

    def draw(self):
        if self.enabled:
            for key, item in self.items.items():
                item.display.draw(self._surface, Object((self.pos[0] * -1, self.pos[1] * -1, 0, 0)))


class MenuItem(Object):
    def __init__(self, rect=(0, 0, 0, 0), rColor=(255, 255, 255), oColor=(0, 0, 0), text="",
                 tColor=(0, 0, 0), action=None, image = False, toggle = False, tGroup = None):
        Object.__init__(self, rect)
        self.action = action
        self.images = [pygame.surface.Surface((self.w, self.h)),
                       pygame.surface.Surface((self.w, self.h))]
        self.tGroup = tGroup
        self.toggle = toggle
        if self.toggle:
            self.togState = 0
        self.display = Display(self.images[0], self, False)

        self.rcolor = rColor
        self.ocolor = oColor
        self.tcolor = tColor
        self.text = text
        self.image = image
        self.update()

    def update(self, Rect=None, RColor=None, OColor=None, Text=None, TColor=None, Image=None):
        if Rect is None:
            Rect = self
        if RColor is None:
            RColor = self.rcolor
        if OColor is None:
            OColor = self.ocolor
        if Text is None:
            Text = self.text
        if TColor is None:
            TColor = self.tcolor
        if Image is None:
            Image = self.image

        colors = [RColor, OColor]
        for i in range(len(colors)):
            self.images[i].fill(colors[i])
            if Text:
                text = pygame.font.Font(None, 25).render(Text, 1, TColor)
                self.images[i].blit(text, ((self.images[i].get_width() / 2) - (text.get_width() / 2), (self.images[i].get_height() / 2) - (text.get_height() / 2)))
            if Image:
                self.images[i].blit(Image, (1, 1))

    def move(self, vect):
        self.x += self.vect[0]
        self.y += self.vect[1]

    def grow(self, dx, dy):
        self.w += dx
        self.h += dy

    def tick(self, input, menu, mPos):
        collide = pygame.Rect(menu[0] + self.x, menu[1] + self.y, self.w, self.h).collidepoint(mPos[0], mPos[1])
        self.display.replace(self.images[collide])
        if self.toggle:
            if self.togState:
                self.display.replace(self.images[1])
        if input == pygame.MOUSEBUTTONDOWN:
            if collide:
                if self.toggle:
                    self.togState = 2
                if self.action is not None:
                    return self.action

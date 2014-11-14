import pygame
from display import Display
from enableable import Enableable
from object import Object


class Menu(Object, Enableable):
    def __init__(self, pos, surface, enabled=True):
        Object.__init__(self, pos[0], pos[1], 0, 0)
        Enableable.__init__(self, enabled)

        self._surface = surface
        self.pos = pos
        self.items = {}

    def select(self, key):
        return self.items.get(key)

    def tick(self, input, mPos):
        t = []
        if self.enabled:
            for item in self.items.values():
                tmp = len(t)
                if len(input) > 0:
                    for event, key in input:
                        eTick = item.tick(event, self, mPos)
                        if eTick is not None:
                            t.append(eTick)
                if len(t) > tmp:
                    for e in self.items.values():
                        if e.toggle:
                            if e.tGroup == item.tGroup:
                                e.togState = {True: 1, False: 0}[e.togState == 2]
                item.tick(0, self, mPos)
        return t

    def addItem(self, key, **kwargs):
        self.items[key] = MenuItem(action=key, **kwargs)

    def draw(self):
        if self.enabled:
            for key, item in self.items.items():
                item.display.draw(self._surface, Object((self.x * -1, self.y * -1, 0, 0)))


class MImage(object):
    def __init__(self, image):
        self._image = image


class MToggle(object):
    def __init__(self, default=False):
        self._toggled = default


class 


class MenuItem(Object):
    def __init__(self, rect=None, rColor=(255, 255, 255), oColor=(0, 0, 0), text="",
                 tColor=(0, 0, 0), action=None, image = False, toggle = False, tGroup = None):
        Object.__init__(self, rect)
        self.action = action
        self.images = [pygame.surface.Surface((self.w, self.h)),
                       pygame.surface.Surface((self.w, self.h))]
        self.tGroup = tGroup
        self.toggle = toggle
        if self.toggle:
            self.togState = 0
        self.display = Display(self.images[0], self)

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
        collide = pygame.Rect(menu.x + self.x, menu.y + self.y, self.w, self.h).collidepoint(mPos[0], mPos[1])
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

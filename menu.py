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

    def addItem(self, key, *args):
        self.items[key] = MenuItem(*args)

    def draw(self):
        if self.enabled:
            for key, item in self.items.items():
                item.display.draw(self._surface,
                                  Object((self.x * -1, self.y * -1, 0, 0)),
                                  False)# animate=item.collided)


class MType(object):
    def update(self, image, **kwargs):
        raise NotImplementedError("Subclasses should override this")

    def tick(self, collide, inputs):
        pass


class MImage(MType):
    def __init__(self, image):
        self._image = image
        super().__init__()

    def update(self, image, **kwargs):
        _image = kwargs.pop("image", None)
        if _image is not None:
            self._image = _image

        for i in range(2):
            image.blit(image, (1, 1 + i * (image.get_height() / 2)))


class MToggle(MType):
    def __init__(self, default=False):
        self._toggled = default
        super().__init__()

    def update(self, image, **kwargs):
        toggle = kwargs.pop("toggle", None)
        if toggle is not None:
            self._toggled = toggle

    def tick(self, collide, inputs):
        if collide and inputs == pygame.MOUSEBUTTONDOWN:
            self._toggled = not self._toggled
        if self._toggled:
            pass
            # self.display.replace(self.images[1])


class MGroup(MType):
    def __init__(self, group):
        self._group = group
        super().__init__()

    def update(self, image, **kwargs):
        group = kwargs.pop("group", None)
        if group is not None:
            self._group = group


class MText(MType):
    def __init__(self, text="", textColor=(0, 0, 0)):
        self._text = text
        self._textColor = textColor
        super().__init__()

    def update(self, image, **kwargs):
        text = kwargs.pop("text", None)
        textColor = kwargs.pop("textColor", None)
        if text is not None:
            self._text = text
        if textColor is not None:
            self._textColor = textColor

        for i in range(2):
            text = pygame.font.Font(None, 25).render(self._text, 1, self._textColor)
            quarterH = image.get_height() / 4
            image.blit(text,
                       ((image.get_width() / 2) - (text.get_width() / 2),
                        (quarterH + quarterH * 2 * i) - (text.get_height() / 2)))


class MAction(MType):
    def __init__(self, action, *args):
        self._action = action
        self._args = args
        super().__init__()

    def update(self, image, **kwargs):
        action = kwargs.pop("action", None)
        args = kwargs.pop("args", None)
        if action:
            self._action = action
        if args:
            self._args = args

    def tick(self, collide, inputs):
        if collide and inputs == pygame.MOUSEBUTTONDOWN:
            self._action(*self._args)


class MColor(MType):
    def __init__(self, rColor=(255, 255, 255), oColor=(0, 0, 0)):
        self._rColor = rColor
        self._oColor = oColor

    def update(self, image, **kwargs):
        rColor = kwargs.pop("rColor", None)
        oColor = kwargs.pop("oColor", None)
        if rColor is not None:
            self._rColor = rColor
        if oColor is not None:
            self._oColor = oColor

        image.subsurface(Object(image.get_width(), 0)).fill(self._rColor)
        image.subsurface(Object(image.get_width(), image.get_height() / 2)).fill(self._oColor)


class MenuItem(Object):
    def __init__(self, rect=None, *types):
        Object.__init__(self, rect)
        self._selected = False
        self._types = types
        self.display = Display(pygame.surface.Surface((self.w, self.h * 2)), self, anim=2)
        self.update()

    def update(self, **kwargs):
        rect = kwargs.pop("rect", None)
        # if rect:
        #     self.rect = rect
        for typ in self._types:
            typ.update(self.display.getImage(), **kwargs)

    def tick(self, inputs, menu, mPos):
        collide = pygame.Rect(menu.x + self.x, menu.y + self.y,
                              self.w, self.h).collidepoint(mPos[0], mPos[1])
        # self.collided = collide == collide
        # self.display.replace(self.images[collide])
        for typ in self._types:
            typ.tick(collide, inputs)

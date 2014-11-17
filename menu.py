import pygame
from animation import Animation
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

    def tick(self, inputs):
        leftOver = []
        if self.enabled():
            for event in inputs:
                matched = False
                for item in self.items.values():
                    if item.tick(self, event):
                        matched = True

                if not matched:
                    leftOver.append(event)
                # if len(t) > tmp:
                #     for e in self.items.values():
                #         if e.toggle:
                #             if e.tGroup == item.tGroup:
                #                 e.togState = {True: 1, False: 0}[e.togState == 2]
                # item.tick(0, self, mPos)
        return leftOver

    def addItem(self, key, *args):
        self.items[key] = MenuItem(*args)

    def draw(self):
        if self.enabled():
            for key, item in self.items.items():
                item.display.draw(self._surface,
                                  Object((self.x * -1, self.y * -1, 0, 0)))


class MType(object):
    def update(self, image, **kwargs):
        raise NotImplementedError("Subclasses should override this")

    def getCollide(self, collide):
        return False

    def tick(self, display, collide, event):
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
            image.blit(image, (i * (image.get_width() / 2), 0))


class MToggle(MType):
    def __init__(self, default=False):
        self._toggled = default
        super().__init__()

    def update(self, image, **kwargs):
        toggle = kwargs.pop("toggle", None)
        if toggle is not None:
            self._toggled = toggle

    def getCollide(self, collide):
        return self._toggled

    def tick(self, display, collide, event):
        if collide and event.type == pygame.MOUSEBUTTONDOWN:
            self._toggled = not self._toggled


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
            quarterW = image.get_width() / 4
            image.blit(text,
                       (int(quarterW + quarterW * 2 * i - (text.get_width() / 2)),
                        int((image.get_height() / 2) - (text.get_height() / 2))))


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

    def tick(self, display, collide, event):
        if collide and event.type == pygame.MOUSEBUTTONDOWN:
            self._action(*self._args)


class MColor(MType):
    def __init__(self, rColor=(255, 255, 255), oColor=(0, 0, 0)):
        self._rColor = rColor
        self._oColor = oColor
        self._rImage = None
        self._oImage = None

    def update(self, image, **kwargs):
        rColor = kwargs.pop("rColor", None)
        oColor = kwargs.pop("oColor", None)
        if rColor is not None:
            self._rColor = rColor
        if oColor is not None:
            self._oColor = oColor

        width = image.get_width()
        height = image.get_height()
        self._rImage = image.subsurface(Object(width / 2, height)).fill(self._rColor)
        self._oImage = image.subsurface(Object(width / 2, 0, width / 2, height)).fill(self._oColor)

    def tick(self, display, collide, event):
        if collide:
            display.replace(self._oImage)
        else:
            display.replace(self._rImage)


class MenuItem(Object):
    def __init__(self, rect=None, *types):
        Object.__init__(self, rect)
        self._selected = False
        self._collided = False
        self._types = types

        image = pygame.surface.Surface((self.w * 2, self.h))
        self.display = Display(image, self)
        self.update()

        anim = Animation(image, 2, self.collided, None, None)
        anim.build()
        self.display.addAnimation(anim)

    def update(self, **kwargs):
        rect = kwargs.pop("rect", None)
        # if rect:
        #     self.rect = rect
        for typ in self._types:
            typ.update(self.display.getImage(), **kwargs)

    def collided(self):
        for typ in self._types:
            if typ.getCollide(self._collided):
                return True
        return self._collided

    def tick(self, menu, event):
        collide = pygame.Rect(menu.x + self.x, menu.y + self.y,
                              self.w, self.h).collidepoint(event.pos[0], event.pos[1])
        self._collided = collide

        for typ in self._types:
            typ.tick(self.display, collide, event)

        return collide

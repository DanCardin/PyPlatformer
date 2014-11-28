import pygame
from animation import Animation
from display import Display, Drawable
from enableable import Enableable
from object import Object
from surface import Surface


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
        return leftOver

    def addItem(self, key, *args):
        self.items[key] = MenuItem(*args)

    def addGroup(self, key, *args):
        self.items[key] = ItemGroup(*args)

    def appendGroup(self, key, *args):
        self.items[key].appendItems(*args)

    def draw(self):
        if self.enabled():
            for key, item in self.items.items():
                item.draw(self._surface, Object(self.x * -1, self.y * -1, 0, 0))


class ItemGroup(Drawable):
    def __init__(self, *args):
        self._items = []
        self._selected = None
        self._groupSelect = MSelected()

        self.appendItems(*args)

    def draw(self, surface, camera):
        for item in self._items:
            item.draw(surface, camera)

    def appendItems(self, *args):
        for item in args:
            assert isinstance(item, MenuItem)

        self._items.extend(args)

    def tick(self, menu, event):
        for item in self._items:
            if item.tick(menu, event):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if item is not self._selected:
                        if self._selected is not None:
                            self._selected.remove(MSelected)
                        item.update(self._groupSelect)
                        self._selected = item
                    event = None

        return event is None


class MType(object):
    def update(self, image):
        pass

    def getCollide(self, collide):
        return False

    def tick(self, display, collide, event):
        pass


class MSelected(MType):
    def getCollide(self, collide):
        return True


class MAlpha(MType):
    def __init__(self, alpha):
        self._alpha = alpha
        super().__init__()

    def update(self, image):
        image.set_alpha(self._alpha)


class MImage(MType):
    def __init__(self, image):
        self._image = image
        super().__init__()

    def update(self, image):
        for i in range(2):
            # image.blit(self._image, (i * (image.get_width() / 2), 0))
            image.blit(self._image, (0, 0))


class MText(MType):
    def __init__(self, text="", textColor=(0, 0, 0)):
        self._text = text
        self._textColor = textColor
        super().__init__()

    def update(self, image):
        for i in range(2):
            text = pygame.font.SysFont("arial", 25).render(self._text, 1, self._textColor)
            quarterW = image.get_width() / 4
            image.blit(text,
                       (int(quarterW + quarterW * 2 * i - (text.get_width() / 2)),
                        int((image.get_height() / 2) - (text.get_height() / 2))))


class MAction(MType):
    def __init__(self, action, *args):
        self._action = action
        self._args = args
        super().__init__()

    def tick(self, display, collide, event):
        if collide and event.type == pygame.MOUSEBUTTONDOWN:
            self._action(*self._args)


class MColor(MType):
    def __init__(self, rColor=(255, 255, 255), oColor=(0, 0, 0)):
        self._rColor = rColor
        self._oColor = oColor
        self._rImage = None
        self._oImage = None

    def update(self, image):
        width = image.get_width()
        height = image.get_height()
        self._rImage = image.subsurface(Object(width / 2, height).asRect()).fill(self._rColor)
        self._oImage = image.subsurface(Object(width / 2, 0, width / 2, height).asRect()).fill(self._oColor)

    def tick(self, display, collide, event):
        if collide:
            display.replace(self._oImage)
        else:
            display.replace(self._rImage)


class MenuItem(Object, Drawable):
    def __init__(self, rect, *types):
        Object.__init__(self, rect)
        self._selected = False
        self._collided = False
        self._types = {}
        self._applicable = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]

        image = Surface((self.w * 2, self.h))
        self._display = Display(image, self)
        self.update(*types)

        anim = Animation(image, 2, self.collided, None, None)
        anim.build()
        self._display.addAnimation(anim)

    def remove(self, arg):
        self._types.pop(arg)

    def update(self, *args):
        for arg in args:
            if isinstance(arg, MType):
                self._types[arg.__class__] = arg
                arg.update(self._display.getImage())
            else:
                raise ValueError("Unrecognized type", arg)

    def collided(self):
        for typ in self._types.values():
            if typ.getCollide(self._collided):
                return True
        return self._collided

    def tick(self, menu, event):
        collide = False
        if event and event.type in self._applicable:
            collide = pygame.Rect(menu.x + self.x, menu.y + self.y,
                                  self.w, self.h).collidepoint(event.pos[0], event.pos[1])
            self._collided = collide

        for typ in self._types.values():
            typ.tick(self._display, collide, event)

        return collide

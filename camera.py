from python.surface import Surface
from display import Display
from object import Object


class Camera(Object):
    def __init__(self, surface, size, maxBounds, boundBox, target):
        Object.__init__(self, size)

        self._surface = surface
        self._display = Display(Surface((self.w, self.h)))
        self._maxBounds = Object(maxBounds)
        self._boundBox = Object(boundBox)
        self._target = target
        assert target is not None

    def tick(self):
        if self.x > self._target.x - self._boundBox.x:
            self.x = self._target.x - self._boundBox.x
        if self.x < self._target.x + self._target.w + self._boundBox.w - self.w:
            self.x = self._target.x + self._target.w + self._boundBox.w - self.w

        if self.x < 0:
            self.x = 0
        if self.x + self.w > self._maxBounds.w:
            self.x = self._maxBounds.w - self.w
        if (self.x < 0) and (self.x + self.w > self._maxBounds.w):
            self.x = self._target.x + self._target.w / 2 - self.w / 2

        if self.y > self._target.y - self._boundBox.y:
            self.y = self._target.y - self._boundBox.y
        if self.y < self._target.y + self._target.h + self._boundBox.h - self.h:
            self.y = self._target.y + self._target.h + self._boundBox.h - self.h

        if self.y < 0:
            self.y = 0
        if self.y + self.h > self._maxBounds.h:
            self.y = self._maxBounds.h - self.h
        if (self.y < 0) and (self.y + self.h > self._maxBounds.h):
            self.y = self._target.y + self._target.h / 2 - self.h / 2

    def draw(self, surface):
        """Calculate the scaling and whatnot"""
        self.
        self.display.draw(surface)

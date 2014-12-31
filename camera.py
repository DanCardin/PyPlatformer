from pygame import transform
from display import Display
from object import Object, ScaledObject, ScaledOffsetObject
from scaleable import Scaled
from surface import Surface


class Camera(ScaledObject, Scaled):
    def __init__(self, size, scale, boundBox, maxBounds, target):
        super().__init__(size=size, scale=scale)

        self._boundBox = ScaledOffsetObject(rect=boundBox, scale=self.getScale)
        """The bounding box inside which the target must stay, relative to the
           `size` of the camera"""

        self._maxBounds = maxBounds
        """The bounds inside which the `Camera  itself must stay"""

        self._target = target
        """The object that the camera follows"""

        self._display = Display(Surface(size))
        self._displaySurfaceCache = self._display.getImage()
        self._surfaceCache = None

        self._lastScale = None

        assert target is not None

    def getAbsolutePos(self, pos):
        return self.x + (pos[0] * self.getScale()), self.y + (pos[1] * self.getScale())

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

    def draw(self, surface, total_surface):
        """Calculate the scaling and display to the inputted surface"""
        scale = self.getScale()
        if scale != 1:
            if scale != self._lastScale:
                self._surfaceCache = Surface((self.w, self.h))
            self._surfaceCache.blit(total_surface, (-self.x, -self.y))

            scaleTo = self.unscaled()
            transform.scale(self._surfaceCache, (scaleTo.w, scaleTo.h), self._displaySurfaceCache)
            self._lastScale = scale
        else:
            import time
            if time.time() % 2 > 1.9:
                print(self._boundBox, self.asRect())
            self._display.update(total_surface, Display.translate(total_surface.get_rect(), self))

        self._display.draw(surface)

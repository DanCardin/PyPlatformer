from pygame import transform
from display import Display
from object import Object, ScaledObject, ScaledOffsetObject
from scaleable import Scaled
from surface import Surface


class Viewport(ScaledObject, Scaled):
    """
    A `Scaleable` view onto some object.
    """
    def __init__(self, size, scale, target=None, boundBox=Object(), maxBounds=None):
        """
        `size` - The size (width and height).
        `scale` - The scale at which to render the view.
        `target` - (Optional) An object that the position of the `Viewport` should follows. If
                   not set, the `Viewport` will not move automatically.
        `boundBox` - (Optional) A sub-view of the `Viewport`, inside which the `target` should
                     always remain. If not set, it will be set to the Viewport's size.
        `maxBounds` - (Optional) A Rectangle inside of which the `Viewport` should always remain.
                      If not set, there will be no max/min bounds on the position of the `Viewport`.
        """
        super().__init__(size=size, scale=scale)

        self._target = target
        self._boundBox = ScaledOffsetObject(rect=boundBox, scale=self.getScale)
        self._maxBounds = maxBounds

        self._display = Display(Surface(size))
        self._displaySurfaceCache = self._display.getImage()
        self._surfaceCache = None

        self._lastScale = None

    def getAbsolutePos(self, pos):
        """
        Returns the `pos` converted into terms of the `Viewport`.

        This is important when the scale is not 1 because the on-screen position will not
        match the actual position being passed in at arbitrary scales.
        """
        return self.x + (pos[0] * self.getScale()), self.y + (pos[1] * self.getScale())

    def tick(self):
        """
        Adjusts the position of the `Viewport` to keep the `target` inside `boundBox`, and
        to keep the `Viewport` inside `maxBounds`.
        """

        # Adjusts x and y to relative to the target.
        if self._target:
            if self.x > self._target.x - self._boundBox.x:
                self.x = self._target.x - self._boundBox.x
            if self.x < self._target.x + self._target.w + self._boundBox.w - self.w:
                self.x = self._target.x + self._target.w + self._boundBox.w - self.w

            if self.y > self._target.y - self._boundBox.y:
                self.y = self._target.y - self._boundBox.y
            if self.y < self._target.y + self._target.h + self._boundBox.h - self.h:
                self.y = self._target.y + self._target.h + self._boundBox.h - self.h

        # Adjusts x and y relative to the maximum/minimum bounds.
        if self._maxBounds:
            if self.x < self._maxBounds.x:
                self.x = self._maxBounds.x
            if self.x + self.w > self._maxBounds.w:
                self.x = self._maxBounds.w - self.w
            if (self.x < 0) and (self.x + self.w > self._maxBounds.w):
                self.x = self._target.x + self._target.w / 2 - self.w / 2

            if self.y < self._maxBounds.y:
                self.y = self._maxBounds.y
            if self.y + self.h > self._maxBounds.h:
                self.y = self._maxBounds.h - self.h
            if (self.y < 0) and (self.y + self.h > self._maxBounds.h):
                self.y = self._target.y + self._target.h / 2 - self.h / 2

    def draw(self, surface, total_surface):
        """
        Calculate the scaling and display to the inputted surface.

        `surface` - The `Surface` being drawn to.
        `total_surface` - The `Surface` being copied from.
        """
        scale = self.getScale()

        # Optimization, no need to do scaling when the scale is 1.
        if scale == 1:
            self._display.update(total_surface, Display.translate(total_surface.get_rect(), self))
        else:
            # Optimization, caches the `Surface` object so long as the scale isn't changing.
            if scale != self._lastScale:
                self._surfaceCache = Surface((self.w, self.h))
            self._surfaceCache.blit(total_surface, (-self.x, -self.y))

            scaleTo = self.unscaled()
            transform.scale(self._surfaceCache, (scaleTo.w, scaleTo.h), self._displaySurfaceCache)
            self._lastScale = scale

        self._display.draw(surface)

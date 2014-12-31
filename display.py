from object import Object
from files import Files


class Drawable(object):
    """
    An interface for things that want to be able draw(...)
    """
    def draw(self, surface, camera=Object()):
        """
        Draws the Superclass' `Display`.

        `surface` - The surface being drawn to.
        `camera` - An `Object` which the `Display` will be drawn relative to.
        """
        self._display.draw(surface, camera)


class Display(Drawable):
    """
    A drawable image that can be animated.
    """
    @staticmethod
    def translate(rect, cam):
        """
        Converts the `rect`'s position to be relative to the `cam`.
        """
        return Object(rect=(rect.x - cam.x, rect.y - cam.y, rect.w, rect.h))

    def __init__(self, surface, klass=None, anim=None, transparent=False, alpha=None):
        """
        `surface` - A `Surface` that will be what's drawn when `self` is displayed.
        `klass` - (Optional) The parent class of the `Suface` being drawn (used for absolute
                  positioning of the draw).
        `anim` - (Optional) An `Animation` object to associate with the `Display`. This will
                 animate the `surface` on each call to `draw(...)`.
        `transparent` - (Optional) Allows for a transparent colorkey to be set. If `True`, the
                        color of the top-left-most pixel's color will be used. Otherwise the
                        supplied color will be used.
        `alpha` - (Optional) An integer between 0 and 255 to specify an alpha for the `surface`.
        """
        self._image = surface
        self._klass = klass
        if klass is None and self._image:
            self._klass = self._image.get_rect()

        if transparent:
            if transparent is True:
                self._image.set_colorkey(self._image.get_at((0, 0)))
            else:
                self._image.set_colorkey(transparent)

        if alpha is not None:
            self._image.set_alpha(alpha)

        self._animation = anim
        if self._animation:
            self._animation.build()
            self.replace(self._animation.animate())

    def getImage(self):
        """
        Returns the `Surface` of the `Display`.
        """
        return self._image

    def update(self, source, dest, area=None):
        """
        Directly blits the `source` to the position, `dest` (with an area, `area`) on the `Surface`.
        """
        self._image.blit(source, dest.asRect(), area.asRect() if area else None)

    def replace(self, image):
        """
        Replaces the `Display`'s `Surface` with `image`.
        """
        self._image = image

    def draw(self, surface, camera=Object()):
        """
        Draws the `Display`'s `Surface` to `surface`.

        `surface` - The surface being drawn to.
        `camera` - An `Object` which the `Display` will be drawn relative to.
        """
        if self._animation:
            self.replace(self._animation.animate())
        rect = Display.translate(self._klass, camera)
        surface.blit(self._image, (rect.x, rect.y))

    def addAnimation(self, animation):
        """
        Adds or replaces an existing `Animation` to the `Display`.
        """
        self._animation = animation

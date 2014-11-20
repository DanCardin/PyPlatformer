from animation import Animation
from object import Object
from files import Files


class Display(object):
    @staticmethod
    def translate(rect, cam):
        return Object((rect.x - cam.x, rect.y - cam.y, rect.w, rect.h))

    def __init__(self, surface=None, klass=None, transparent=False, anim=None, alpha=None):
        self._image = Files.loadImage(surface) if isinstance(surface, str) else surface
        self._klass = klass
        if klass is None and self._image:
            self._klass = self._image.get_rect()

        if transparent:
            self._image.set_colorkey(self._image.get_at((0, 0)))
        if alpha is not None:
            self._image.set_alpha(alpha)

        self._animation = anim
        if self._animation:
            self._animation.build()
            self.replace(self._animation.animate())

    def getImage(self):
        return self._image

    def update(self, *args):
        self._image.blit(*args)

    def replace(self, image):
        self._image = image

    def draw(self, surface, camera=Object()):
        if self._animation:
            self.replace(self._animation.animate())
        rect = Display.translate(self._klass, camera)
        surface.blit(self._image, rect)

    def addAnimation(self, animation):
        self._animation = animation


class Drawable(object):
    def draw(self, surface, camera=Object()):
        self._display.draw(surface, camera)

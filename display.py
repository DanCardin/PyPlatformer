from pygame.surface import Surface
from animation import Animation
from object import Object
from files import Files


class Display(object):
    def __init__(self, surface, klass=None, transparent=False, anim=None, alpha=0):
        if isinstance(surface, str):
            self._image = Surface((klass.w, klass.h))
            self._image.blit(Files().loadImage(surface), (0, 0))
        else:
            self._image = surface

        self._klass = klass if klass else self._image.get_rect()
        if transparent:
            self._image.set_colorkey(self._image.get_at((0, 0)))
        if alpha:
            self._image.set_alpha(alpha)
        self._animation = Animation(self, self._image, anim) if anim else None

    def getImage(self):
        return self._image

    def update(self, *args):
        self._image.blit(*args)

    def replace(self, image):
        self._image = image

    def draw(self, surface, camera=Object((0, 0))):
        if self._animation:
            self._animation.animate(self._klass.move.getDir(x=True))
        rect = self.translate(self._klass, camera)
        surface.blit(self._image, rect)

    def translate(self, rect, Cam):
        return Object((rect.x - Cam.x, rect.y - Cam.y, rect.w, rect.h))

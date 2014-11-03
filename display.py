import pygame
from animation import Animation
from files import Files


class Display(object):
    def __init__(self, surface, klass, transparent=False, anim=None, alpha=0):
        self._klass = klass
        if isinstance(surface, str):
            self._image = pygame.surface.Surface((self._klass.w, self._klass.h))
            self._image.blit(Files().loadImage(surface), (0, 0))
        else:
            self._image = surface
        if transparent:
            self._image.set_colorkey(self._image.get_at((0, 0)))
        if alpha:
            self._image.set_alpha(75)
        self._animation = Animation(self, self._image, anim) if anim else None

    def update(self, *args):
        self._image.blit(*args)

    def replace(self, image):
        self._image = image

    def draw(self, surface, camera):
        if self._animation:
            self._animation.animate(self._klass.move.getDir(x=True))
        rect = self.translate(self._klass, camera)
        surface.blit(self._image, rect)

    def translate(self, rect, Cam):
        return pygame.Rect(rect.x - Cam.x, rect.y - Cam.y, rect.w, rect.h)

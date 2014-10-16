import pygame
from animation import *
from files import *


class Display(object):
    def __init__(self, surface, klass, transparent, anim=None):
        self.klass = klass
        if isinstance(surface, str):
            image = Files().loadImage(surface)
            self.image = pygame.surface.Surface((self.klass.w, self.klass.h))
            self.image.blit(image, (0, 0))
        else:
            self.image = surface
        self.animation = Animation(image, anim, self.klass) if anim else None
        if transparent:
            self.transColor = self.image.get_at((0, 0))
            self.image.set_colorkey(self.transColor)

    def updateImage(self, *args):
        self.image.blit(*args)

    def draw(self, surface, camera):
        if self.animation:
            self.animation.animate(1)
        rect = self.translate(self.klass, camera)
        surface.blit(self.image, rect)

    def translate(self, rect, Cam):
        return pygame.Rect(rect.x - Cam.x, rect.y - Cam.y, rect.w, rect.h)

import pygame
from animation import *
from files import *


class Display(object):
    def __init__(self, tileset, klass, size, transparent, anim=(False, 1)):
        self.klass = klass
        if isinstance(tileset, str):
            image = Files().loadImage(tileset)
            self.image = pygame.surface.Surface((size[2], size[3]))
            self.image.blit(image, (0, 0))
        else:
            self.image = tileset
        if anim[0]:
            self.animation = Animation(image, anim[1], self.klass)
        self.trans = transparent
        if self.trans:
            self.transColor = self.image.get_at((0, 0))
            self.image.set_colorkey(self.transColor)

    def changeImage(self, image, pos):
        """"""

    def draw(self, surface, camera):
        if hasattr(self, "animation"):
            self.animation.animate(1)
        rect = self.translate(self.klass, camera)
        surface.blit(self.image, rect)

    def translate(self, rect, Cam):
        return pygame.Rect(rect.x - Cam.x, rect.y - Cam.y, rect.w, rect.h)

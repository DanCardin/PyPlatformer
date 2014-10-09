import pygame
from animation import *
from files import *


class Display(object):
    def __init__(self, Tileset, classs, Size, Transparent, Anim=(False, 1)):
        self.Class = classs
        if isinstance(Tileset, str):
            self.fileMod = Files()
            image = self.fileMod.loadImage(Tileset)
            self.image = pygame.surface.Surface((Size[2], Size[3]))
            self.image.blit(image, (0, 0))
        else:
            self.image = Tileset
        if Anim[0]:
            self.animation = Animation(image, Anim[1], self.Class)
        self.trans = Transparent
        if self.trans:
            self.transColor = self.image.get_at((0, 0))
            self.image.set_colorkey(self.transColor)

    def draw(self, surface, camera):
        if hasattr(self, "animation"):
            self.animation.animate(1)
        rect = self.translate(self.Class, camera)
        surface.blit(self.image, rect)

    def translate(self, rect, Cam):
        return pygame.Rect(rect.x - Cam.x, rect.y - Cam.y, rect.w, rect.h)

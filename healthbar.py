import pygame
from char import Health


class HealthBar(object):
    def __init__(self, x, y, parent):
        assert isinstance(parent, Heath)

        self._parent = parent

        
        surf = pygame.surface.Surface()
        self._display()

    def 

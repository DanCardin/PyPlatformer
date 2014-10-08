#!/user/bin/env python
import pygame
import os
from game import Game
from const import *

#--- Inits
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init
pygame.font.init()
clock = pygame.time.Clock()

#--- Object Creation
pygame.display.set_caption(gameName)
screen = pygame.display.set_mode((screenSize[0] * res, screenSize[1] * res))
game = Game([(levelFile, tilesetFile)])

#--- Main Loop
while game.started:
    game.tick(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
sys.exit()

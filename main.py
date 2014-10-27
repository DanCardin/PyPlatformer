#!/user/bin/env python
import os
import sys
import pygame
import const
from game import Game

# --- Inits
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# --- Object Creation
pygame.display.set_caption(const.gameName)
screen = pygame.display.set_mode((const.screenSize[0] * const.res,
                                  const.screenSize[1] * const.res))
game = Game(screen, const.levelFiles)

# --- Main Loop
while game.started:
    game.tick()
    clock.tick(const.FPS)
    pygame.display.flip()
pygame.quit()
sys.exit()

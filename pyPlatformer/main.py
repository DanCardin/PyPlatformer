#!/user/bin/env python
import sys
import pygame
import const as const
from game import Game


def run():
    """
    Starts the game, and cleanly exits when it's done.
    """
    game = Game(const.levelFiles)

    while not game.isComplete():
        game.tick()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run()

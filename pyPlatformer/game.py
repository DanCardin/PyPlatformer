import os
import pygame
import const
from collections import namedtuple
from complete import Completable
from enableable import Enableable
from input import Input, Inputable
from menu import Menu, MColor, MText, MAction
from world import World


class Game(Enableable, Completable, Inputable):
    def __init__(self, levels):
        super().__init__()

        # --- Inits
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption(const.gameName)
        self._surface = pygame.display.set_mode((const.screenSize[0] * const.res,
                                                 const.screenSize[1] * const.res))
        self._clock = pygame.time.Clock()
        self._levAttr = levels
        self._world = None
        self._paused = False

        self._menu = Menu(surface=self._surface,
                          pos=(const.screenSize[0] * const.res / 2 - 50,
                               const.screenSize[1] * const.res / 2 - 100),
                          inputStream=self.getInputStream())
        self._menu.addItem("resume", (0, 0, 100, 48), MColor((255, 0, 0), (0, 0, 255)),
                           MText("Resume", (0, 255, 0)), MAction(self._resume))
        self._menu.addItem("start", (0, 50, 100, 48), MColor((255, 0, 0), (0, 0, 255)),
                           MText("Start", (0, 255, 0)), MAction(self.start))
        self._menu.addItem("editor", (0, 100, 100, 48), MColor((255, 0, 0), (0, 0, 255)),
                           MText("Editor", (0, 255, 0)), MAction(self._editor))
        self._menu.addItem("exit", (0, 150, 100, 48), MColor((255, 0, 0), (0, 0, 255)),
                           MText("Exit", (0, 255, 0)), MAction(self.setFinished))

        self._input = Input(inputStream=self.getInputStream())
        self._input.set(pygame.KEYDOWN, self._menuToggle, pygame.K_m)
        self._input.set(pygame.KEYDOWN, self._pause, pygame.K_p)

    def start(self):
        self.enable()
        self._world = World(self._surface, self._levAttr, inputStream=self.getInputStream())
        self._world.nextLevel()
        self._menu.disable()

    def _pause(self):
        self._paused = not self._paused

    def _resume(self):
        if self._world is not None and not self._world.isComplete():
            self.enable()
        else:
            self.start()
        self._menu.disable()

    def _editor(self):
        if self._world:
            self._world.level.editor.enabled()
            self._menu.disable()

    def _menuToggle(self):
        self._menu.toggleEnabled()
        self.toggleEnabled()

    def tick(self):
        self.getEvents()
        self._input()

        if self._menu.enabled():
            self._menu.tick()
            self._menu.draw()
        elif self.enabled:
            if self._world.isComplete():
                if self._world.isFinished():
                    self._win()
                elif self._world.isLost():
                    self._gameOver()
            else:
                if not self._paused:
                    self._world.tick()
        self.clearInputStream()

        self._clock.tick(const.FPS)
        pygame.display.flip()

    def _win(self):
        self._endGame("YOU WIN!")

    def _gameOver(self):
        self._endGame("GAME OVER!")

    def _endGame(self, text):
        try:
            self.__gameOverCount += 1
        except AttributeError:
            self.__gameOverCount = 1
            self.__goText = pygame.font.Font(None, 100).render(text, 1, (255, 0, 0))
            self.__gameOverX = int(self._surface.get_width() / 2 - self.__goText.get_width() / 2)
            self.__gameOverY = int(self._surface.get_height() / 2 - self.__goText.get_height() / 2)

        if self.__gameOverCount < (const.FPS * 5):
            self._surface.fill((0, 0, 0))
            self._surface.blit(self.__goText, (self.__gameOverX, self.__gameOverY))
        else:
            self.__gameOverCount = 0
            self._surface.fill((0, 0, 0))
            self._menuToggle()

    Event = namedtuple("Event", "type key pos")
    def getEvents(self):
        result = self.getInputStream()
        for event in pygame.event.get():
            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                result.append(Game.Event(event.type, event.key, None))

            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                result.append(Game.Event(event.type, None, event.pos))

            if event.type == pygame.QUIT:
                self.setFinished()

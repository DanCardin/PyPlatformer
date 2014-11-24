import pygame
import const
from libs.complete import Completeable
from enableable import Enableable
from input import Input
from menu import Menu, MColor, MText, MAction
from world import World


class Game(Enableable, Completeable):
    def __init__(self, surface, levels):
        Enableable.__init__(self)
        Completeable.__init__(self)

        self._surface = surface
        self._levAttr = levels
        self._world = None

        self._menu = Menu((const.screenSize[0] * const.res / 2 - 50,
                          const.screenSize[1] * const.res / 2 - 100),
                          self._surface)
        self._menu.addItem("resume", (0, 0, 100, 48), MColor((255, 0, 0), (0, 0, 255)),
                           MText("Resume", (0, 255, 0)), MAction(self._resume))
        self._menu.addItem("start", (0, 50, 100, 48), MColor((255, 0, 0), (0, 0, 255)),
                           MText("Start", (0, 255, 0)), MAction(self.start))
        self._menu.addItem("editor", (0, 100, 100, 48), MColor((255, 0, 0), (0, 0, 255)),
                           MText("Editor", (0, 255, 0)), MAction(self._editor))
        self._menu.addItem("exit", (0, 150, 100, 48), MColor((255, 0, 0), (0, 0, 255)),
                           MText("Exit", (0, 255, 0)), MAction(self.setFinished))

        self._input = Input()
        self._input.set(pygame.KEYDOWN, pygame.K_m, "menu", self._menuToggle)

    def start(self):
        self.enable()
        self._world = World(self._surface, self._levAttr)
        self._world.nextLevel()
        self._menu.disable()

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
        inputs = self.getEvents()
        self._input(inputs)
        if self._menu.enabled():
            self._menu.tick(inputs)
            self._menu.draw()
        elif self.enabled:
            if self._world.isComplete():
                if self._world.isFinished():
                    self._win()
                elif self._world.isLost():
                    self._gameOver()
            else:
                self._world.tick(inputs)

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

    def getEvents(self):
        result = []
        for event in pygame.event.get():
            if event.type in [pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN,
                              pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                result.append(event)
            if event.type == pygame.QUIT:
                self.setFinished()
        return result

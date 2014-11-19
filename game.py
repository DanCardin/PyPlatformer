import pygame
import const
from enableable import Enableable
from input import Input
from menu import Menu, MColor, MText, MAction
from world import World


class Game(Enableable):
    def __init__(self, surface, levels):
        Enableable.__init__(self, True)
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
                           MText("Exit", (0, 255, 0)), MAction(self.disable))

        self._input = Input()
        self._input.set(pygame.KEYDOWN, pygame.K_m, "menu", self._menu)

    def start(self):
        self.enable()
        self._world = World(self._surface, self._levAttr)
        self._world.nextLevel()
        self._menu.disable()

    def _resume(self):
        if self._world is not None:
            self.enable()
        else:
            self.start()
        self._menu.disable()

    def _editor(self):
        if self._world:
            self._world.level.enabled()
            self._menu.disable()

    def _menu(self):
        self._menu.toggleEnabled()
        self.toggleEnabled()

    def tick(self):
        inputs = self.getEvents()
        self._input(inputs)
        if self._menu.enabled():
            self._menu.tick(inputs)
            self._menu.draw()
        elif self.enabled:
            self._world.tick(inputs)

    def getEvents(self):
        result = []
        for event in pygame.event.get():
            if event.type in [pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN,
                              pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                result.append(event)
            if event.type == pygame.QUIT:
                self.disable()
        return result

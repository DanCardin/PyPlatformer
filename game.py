import pygame
import const
from enableable import Enableable
from input import Input
from menu import Menu, MColor, MText, MAction
from world import World


class Game(Enableable):
    def __init__(self, surface, levels):
        Enableable.__init__(self, False)
        self._surface = surface
        self.levAttr = levels
        self.world = None
        self.camera = None
        self.started = True

        text = ['Resume', 'Start', 'Editor', 'Exit']
        size = (const.screenSize[0] * const.res, const.screenSize[1] * const.res)
        self.menu = Menu((size[0] / 2 - 50, size[1] / 2 - 50 * len(text) / 2),
                         self._surface)
        for i in range(0, len(text)):
            self.menu.addItem(text[i].lower(), (0, 50 * i, 100, 48),
                              MColor((255, 0, 0), (0, 0, 255)),
                              MText(text[i], (0, 255, 0)),
                              MAction(self.handleMenu, text[i].lower()))

        self._input = Input()
        self._input.set(pygame.KEYDOWN, pygame.K_m, "menu", self._menu)

    def start(self):
        self.enable()
        self.world = World(self._surface, self.levAttr)
        self.world.nextLevel()

    def handleMenu(self, action):
        if 'resume' in action:
            if self.world is not None:
                self.enable()
            else:
                self.start()
            self.menu.disable()
        elif 'start' in action:
            self.start()
            self.menu.disable()
        elif 'editor' in action:
            if self.world:
                self.world.level.enabled()
                self.menu.disable()
        elif 'exit' in action:
            self.exit()

    def _menu(self):
        self.menu.toggleEnabled()
        self.toggleEnabled()

    def tick(self):
        inputs = self.getEvents()
        self._input(inputs)
        if self.menu.enabled():
            mPos = pygame.mouse.get_pos()
            self.menu.tick(inputs, mPos)
            self.menu.draw()
        elif self.enabled:
            self.world.tick(inputs)

    def exit(self):
        self.started = False

    def getEvents(self):
        re = []
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                re.append((event.type, event.key))
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                re.append((event.type, event.pos))
        return re

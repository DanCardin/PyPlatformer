import pygame
import const
from world import World
from menu import Menu


class Game(object):
    def __init__(self, surface, levels):
        self._surface = surface
        self.levAttr = levels
        self.world = None
        self.camera = None
        self.enabled = False
        self.started = True

        self._size = (const.screenSize[0] * const.res, const.screenSize[1] * const.res)

        text = ['Resume', 'Start', 'Editor', 'Exit']
        self.menu = Menu(self._surface,
                         (self._size[0] / 2 - 50, self._size[1] / 2 - 50 * len(text) / 2),
                         True)
        for i in range(0, len(text)):
            self.menu.addItem(text[i].lower(), rect=(0, 50 * i, 100, 48),
                              rColor=(255, 0, 0), oColor=(0, 0, 255), text=text[i],
                              tColor=(0, 255, 0))

    def start(self):
        self.enabled = True
        self.world = World(self._surface, self.levAttr)
        self.world.nextLevel()

    def handleMenu(self, action):
        if 'resume' in action:
            if self.world is not None:
                self.enabled = True
            else:
                self.start()
            self.menu.enabled = False
        elif 'start' in action:
            self.start()
            self.menu.enabled = False
        elif 'editor' in action:
            if self.world:
                self.world.level.enabled = True
                self.menu.enabled = False
        elif 'exit' in action:
            self.exit()

    def tick(self):
        inputer = self.getEvents()
        if (pygame.KEYDOWN, pygame.K_m) in inputer:
            self.menu.enabled = not self.menu.enabled
            self.enabled = not self.enabled
        if (pygame.KEYDOWN, pygame.K_r) in inputer:
            self.menu.enabled = False
            self.enabled = True
            self.world.level.start()

        if self.menu.enabled:
            mPos = pygame.mouse.get_pos()
            self.handleMenu(self.menu.tick(inputer, mPos))
            self.menu.draw()
        elif self.enabled:
            self.world.tick(inputer)
            inputer = False

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

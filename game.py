import pygame

from const import *
from world import *
from menu import *


class Game(object):
    def __init__(self, Levels):
        self.levAttr = Levels
        self.world = 0  # World(Levels)
        self.camera = 0
        self.enabled = False
        self.started = True

        text = ['Resume', 'Start', 'Editor', 'Exit']
        self.menu = Menu((screenSize[0] * res / 2 - 50, screenSize[1] * res / 2 - 50 * len(text) / 2), True)
        for i in range(0, len(text)):
            self.menu.addItem(rect=(0, 50 * i, 100, 48), rColor=(255, 0, 0), oColor=(0, 0, 255),
                              text=text[i], tColor=(0, 255, 0), action=text[i].lower())

    def start(self):
        self.enabled = True
        self.world = World(self.levAttr)
        self.world.level.start()

    def handleMenu(self, action):
        if 'resume' in action:
            if self.world != 0:
                self.enabled = True
            else:
                self.start()
            self.menu.enabled = False
        elif 'start' in action:
            self.start()
            self.menu.enabled = False
        elif 'editor' in action:
            if self.started:
                self.world.level.enabled = True
                self.menu.enabled = False
        elif 'exit' in action:
            self.exit()

    def tick(self, surface):
        inputer = self.getEvents()
        if (pygame.KEYDOWN, pygame.K_m) in inputer:
            self.menu.enabled = not self.menu.enabled
            self.enabled = not self.enabled
            print(self.menu.items)
        if (pygame.KEYDOWN, pygame.K_r) in inputer:
            self.menu.enabled = False
            self.enabled = True
            self.world.level.start()

        if self.menu.enabled:
            mPos = pygame.mouse.get_pos()
            self.handleMenu(self.menu.tick(inputer, mPos))
            self.menu.draw(surface)
        elif self.enabled:
            self.world.tick(inputer, surface)
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

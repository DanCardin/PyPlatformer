import pygame
from const import *
from display import *
from menu import *
from object import Object


class Editor(Object):
    def __init__(self, map, Camera):
        super().__init__((0, 0, map.size[0] * res, map.size[1] * res))
        self.map = map
        self.camera = Camera

        self.brush = self.cur = self.bType = 0
        self.painting, self.menuShowing, self.enabled, self.mChange, self.tile = False, True, False, True, False
        self.acmap = pygame.surface.Surface((self.x, self.y))
        self.acmap.set_colorkey((0, 0, 0))
        self.display = Display(self.acmap, self, self.acmap.get_rect(), False)

        self.menu = Menu((0, screenSize[1] * res), False)
        self.menu.addItem(rect=(0, 0, 32, 32), rColor=(255, 0, 0), oColor=(0, 0, 255),
                          text="Save", tColor=(0, 255, 0), action="save")
        self.menu.addItem(rect=(32, 0, 32, 32), rColor=(255, 0, 0), oColor=(0, 0, 255), text="Pen",
                          tColor=(0, 255, 0), action="pen", toggle=True, tGroup=0)
        self.menu.addItem(rect=(64, 0, 32, 32), rColor=(255, 0, 0), oColor=(0, 0, 255), text="Box",
                          tColor=(0, 255, 0), action="box", toggle=True, tGroup=0)
        self.menu.addItem(rect=(96, 0, 100, 32), rColor=(255, 0, 0), oColor=(0, 0, 255),
                          text="Wall", tColor=(0, 255, 0), action="wall", toggle=True, tGroup=1)
        self.menu.addItem(rect=(196, 0, 100, 32), rColor=(255, 0, 0), oColor=(0, 0, 255),
                          text="Empty", tColor=(0, 255, 0), action="empty", toggle=True, tGroup=1)
        for i in range(0, TILE_SET_LENGTH - 1):
            surf = pygame.surface.Surface((30, 30))
            surf.blit(self.map.tileset, pygame.Rect(-1, -i * res, res - 2, res - 2))
            self.menu.addItem(rect=(32 * i, 32, 32, 32), rColor=(255, 0, 0), oColor=(0, 0, 255),
                              action=(i - 1), image=surf, toggle=True, tGroup=2)

    def pen(self, key):
        tile = ((key[0] + self.camera.x) / res, (key[1] + self.camera.y) / res)
        type = {False: self.bType, True: 2}[pygame.K_LCTRL in pygame.key.get_pressed()]
        if self.bType != 0:
            self.map.setType(tile[0], tile[1], type)
        elif self.brush != 0:
            self.map.setTile(tile[0], tile[1], self.brush)

    def box(self, key):
        ''''''

    def handleKeys(self, event, input):
        if input == pygame.K_q:
            self.menuShowing = not self.menuShowing
        if input == pygame.K_RETURN:
            self.map.save()

    def handleMouse(self, event, input):
        if event == pygame.MOUSEBUTTONDOWN:
            self.painting = True
        if event == pygame.MOUSEBUTTONUP:
            self.painting = False

    def handleMenu(self, action, input):
        if action == []:
            for event, key in input:
                if event == pygame.KEYDOWN or event == pygame.KEYUP:
                    self.handleKeys(event, key)
                else:
                    self.handleMouse(event, key)
        if "pen" in action:
            self.bType = 0
        if "box" in action:
            self.bType = 1
        if pygame.K_LCTRL in pygame.key.get_pressed():
            self.bType = 2
        if "save" in action:
            self.map.save()
        for i in range(0, TILE_SET_LENGTH - 1):
            if i in action:
                self.brush = i + 1

    def edit(self, input):
        mPos = pygame.mouse.get_pos()
        self.handleMenu(self.menu.tick(input, mPos), input)
        if self.painting:
            self.mChange = True
            if self.bType == 0:
                self.pen(mPos)
            elif self.bType == 1:
                self.box(mPos)

    def drawMap(self):
        for i in range(self.map.size[0]):
            for e in range(self.map.size[1]):
                col = {0: self.map.transColor,
                       1: (0, 0, 255),
                       2: (0, 255, 0)}[self.map.getType(i, e)]
                if col != self.map.transColor:
                    pygame.draw(self.acmap, col,  (i * res, e * res, res, res))

    def draw(self, surface, camera):
        if self.mChange:
            self.drawMap()
            self.mChange = False
        if self.menuShowing:
            self.display.draw(surface, camera)
        self.menu.draw(surface)

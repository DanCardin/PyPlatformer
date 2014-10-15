import pygame
from const import *
from display import *
from menu import *
from input import *


class Editor(Object):
    def __init__(self, Map, Camera):
        Object.__init__(self, (0, 0, Map.size[0] * res, Map.size[1] * res))
        self.map = Map
        self.camera = Camera
        self.brush = 0
        self.bType = -1
        self.tool = 0
        self.modifier = 0
        self.painting = False
        self.enabled = False
        self.tile = False
        self.menuShowing = True
        self.mChange = True
        self.acmap = pygame.surface.Surface((self.w, self.h))
        self.acmap.set_alpha(75, pygame.RLEACCEL)
        self.acmap.set_colorkey((0, 0, 0))
        self.display = Display(self.acmap, self, self.acmap.get_rect(), False)
        self.input = Input()
        self.input.set(pygame.KEYDOWN, pygame.K_l, "emenu", self.toggleMenu)
        self.input.set(pygame.KEYDOWN, pygame.K_RETURN, "save", self.map.save)
        self.input.set(pygame.KEYDOWN, pygame.K_LCTRL, "start", self.startBlock)
        self.input.set(pygame.KEYDOWN, pygame.K_LSHIFT, "end", self.endBlock)
        self.create()

    def create(self):
        self.menu = Menu((0, screenSize[1] * res), False)
        self.menu.addItem("save", rect=(0, 0, 32, 32), text="Save")
        self.menu.addItem("pen", rect=(32, 0, 32, 32), text="Pen", toggle=True, tGroup=0)
        self.menu.addItem("box", rect=(64, 0, 32, 32), text="Box", toggle=True, tGroup=0)
        self.menu.addItem("tiles", rect=(96, 0, 32, 32), text="Tiles", toggle=True, tGroup=1)
        self.menu.addItem("wall", rect=(196, 0, 100, 32), text="Wall", toggle=True, tGroup=1)
        self.menu.addItem("empty", rect=(296, 0, 100, 32), text="Empty", toggle=True, tGroup=1)
        self.menu.addItem("death", rect=(396, 0, 100, 32), text="Death", toggle=True, tGroup=1)
        self.menu.addItem("collision", rect=(500, 0, 100, 32), text="Coll", toggle=True, tGroup=3)
        self.menu.select("pen").togState = True
        self.menu.select("tiles").togState = True
        for i in range(TILE_SET_LENGTH):
            surf = pygame.surface.Surface((30, 30))
            surf.blit(self.map.tileset, pygame.Rect(-1, -i * res, res - 2, res - 2))
            self.menu.addItem(i, rect=(32 * i, 32, 32, 32), text="", image=surf,
                              toggle=True, tGroup=2)

    def pen(self, key):
        tile = (int((key[0] + self.camera.x) / res), int((key[1] + self.camera.y) / res))
        print(self.bType)
        print(tile)
        if self.bType == -1:
            self.map.setTile(tile[0], tile[1], self.brush)
        elif self.bType >= 0:
            self.map.setType(tile[0], tile[1], self.bType)

    def box(self, input, key):
        if not hasattr(self, "gen"):
            self.gen = 1
        for event, keyy in input:
            if event == pygame.MOUSEBUTTONDOWN:
                self.gen = {-1: 1, 1: -1}[self.gen]

    def toggleMenu(self):
        self.menuShowing = not self.menuShowing

    def startBlock(self):
        self.modifier = 1

    def endBlock(self):
        self.modifier = 2

    def handleMouse(self, event, input):
        return {pygame.MOUSEBUTTONDOWN: True, pygame.MOUSEBUTTONUP: False}.get(event)

    def handleMenu(self, action, inputs):
        self.modifier = 0
        if action == []:
            self.input(inputs)
            for event, key in inputs:
                if not (event == pygame.KEYDOWN or event == pygame.KEYUP):
                    self.painting = self.handleMouse(event, key)

        if "pen" in action:
            self.tool = 0
        if "box" in action:
            self.tool = 1
        if "tiles" in action:
            self.bType = -1

        if "empty" in action:
            self.bType = 0
        if "death" in action:
            self.bType = 4
        if "wall" in action:
            self.menu.items[4].update(OColor=((0, 0, 255)))
            self.bType = 1
        if self.modifier == 1:
            self.menu.items[4].update(OColor=((0, 255, 0)))
            self.bType = 2
        if self.modifier == 2:
            self.menu.items[4].update(OColor=((255, 0, 255)))
            self.bType = 3

        if "save" in action:
            self.map.save()
        if "collision" in action:
            self.menuShowing = not self.menuShowing

        for i in range(TILE_SET_LENGTH):
            if i in action:
                self.brush = i

    def edit(self, inputs):
        mPos = pygame.mouse.get_pos()  # fix it, it doesnt need this because "inputs" already has the mouse pos
        self.handleMenu(self.menu.tick(inputs, mPos), inputs)
        if self.painting:
            self.mChange = True
            if self.tool == 0:
                self.pen(mPos)
            elif self.tool == 1:
                self.box(inputs, mPos)

    def drawMap(self):
        for i in range(self.map.size[0]):
            for e in range(self.map.size[1]):
                col = {0: (0, 0, 0), 1: (0, 0, 255), 2: (0, 255, 0), 3: (255, 0, 255), 4: (255, 0, 0)}[self.map.getType(i, e)]
                if col != self.map.transColor:
                    pygame.draw.rect(self.acmap, col,  (i * res, e * res, res, res))

    def draw(self, surface, camera):
        if self.mChange:
            self.drawMap()
            self.mChange = False
        if self.menuShowing:
            self.display.draw(surface, camera)
        self.menu.draw(surface)
import pygame
import const
from display import *
from menu import *
from input import *
from wall import Tile


class Editor(Object):
    def __init__(self, map, camera):
        Object.__init__(self, (map.w, map.h))
        self.map = map
        self.camera = camera

        self._delta = [(i, e) for e in range(self.map.getSize(y=True))
                        for i in range(self.map.getSize(x=True))]
        self.brush = 0
        self.bType = -1
        self.tool = 0
        self.modifier = 0
        self.painting = False
        self.enabled = False
        self.tile = False
        self.menuShowing = True
        self.mChange = True

        self.display = Display(pygame.surface.Surface((self.w, self.h)), self, True, alpha=True)
        self.input = Input()
        self.input.set(pygame.KEYDOWN, pygame.K_o, "overlay", self.toggleOverlay)
        self.input.set(pygame.KEYDOWN, pygame.K_t, "menu", self.toggleMenu)
        self.input.set(pygame.KEYDOWN, pygame.K_RETURN, "save", self.map.save)
        self.input.set(pygame.KEYDOWN, pygame.K_LCTRL, "start", self.startBlock)
        self.input.set(pygame.KEYDOWN, pygame.K_LSHIFT, "end", self.endBlock)
        self.createMenu()

    def createMenu(self):
        self.menu = Menu((0, const.screenSize[1] * const.res), True)
        self.menu.addItem("save", rect=(0, 0, 32, 32), text="Save")
        self.menu.addItem("pen", rect=(32, 0, 32, 32), text="Pen", toggle=True, tGroup=0)
        self.menu.addItem("box", rect=(64, 0, 32, 32), text="Box", toggle=True, tGroup=0)
        self.menu.addItem("tiles", rect=(96, 0, 32, 32), text="Tiles", toggle=True, tGroup=1)
        self.menu.addItem("wall", rect=(196, 0, 32, 32), text="W", toggle=True, tGroup=1)
        self.menu.addItem("empty", rect=(228, 0, 32, 32), text="V", toggle=True, tGroup=1)
        self.menu.addItem("death", rect=(260, 0, 32, 32), text="D", toggle=True, tGroup=1)
        # self.menu.addItem("start", rect=(292, 0, 32, 32), text="S", toggle=True, tGroup=1)
        # self.menu.addItem("end", rect=(324, 0, 32, 32), text="E", toggle=True, tGroup=1)
        self.menu.addItem("collision", rect=(500, 0, 100, 32), text="Coll", toggle=True, tGroup=3)
        self.menu.select("pen").togState = True
        self.menu.select("wall").togState = True
        ts = self.map.getTileset()
        for i in range(const.TILE_SET_LENGTH):
            surf = pygame.surface.Surface((30, 30))
            surf.blit(ts, pygame.Rect(-1, -i * const.res, const.res - 2, const.res - 2))
            self.menu.addItem(i, rect=(32 * i, 32, 32, 32), image=surf, toggle=True, tGroup=2)

    def pen(self, key):
        block = None
        tile = (int((key[0] + self.camera.x) / const.res),
                int((key[1] + self.camera.y) / const.res))

        try:
            block = self.map.get(tile[0], tile[1])
        except:
            print("Unable to set tile {}.", tile)
        else:
            if self.bType == -1:
                block.setTile(self.brush)
            elif self.bType >= 0:
                block.setType(self.bType)
                self._delta.append(tile)

    def box(self, input, key):
        if not hasattr(self, "gen"):
            self.gen = 1
        for event, keyy in input:
            if event == pygame.MOUSEBUTTONDOWN:
                self.gen = {-1: 1, 1: -1}[self.gen]

    def toggleMenu(self):
        self.menu.enabled = not self.menu.enabled

    def toggleOverlay(self):
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

        for i in range(const.TILE_SET_LENGTH):
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

    def update(self):
        tile = pygame.surface.Surface((const.res, const.res))
        for i, e in self._delta:
            colorKey = {Tile.Empty: (0, 0, 0),
                        Tile.Solid: (0, 0, 255),
                        Tile.Start: (0, 255, 0),
                        Tile.End: (255, 0, 255),
                        Tile.Deadly: (255, 0, 0)}[self.map.get(i, e).getType()]
            tile.fill(colorKey)
            self.display.update(tile, (i * const.res, e * const.res))
        self._delta = []

    def draw(self, surface, camera):
        if self._delta:
            self.update()
        if self.menuShowing:
            self.display.draw(surface, camera)
        self.menu.draw(surface)

import pygame
import const
from display import Display
from enableable import Enableable
from object import Object
from menu import Menu, MText, MToggle, MAction, MGroup, MImage, MColor
from input import Input
from wall import Tile


class Editor(Object, Enableable):
    def __init__(self, map, surface):
        Object.__init__(self, (map.w, map.h + const.res))
        Enableable.__init__(self, False)

        self._map = map
        self._delta = [(i, e) for e in range(self._map.getSize(y=True))
                       for i in range(self._map.getSize(x=True))]
        self.brush = 0
        self.bType = -1
        self.tool = 0
        self.modifier = 0
        self.painting = False
        self.tile = False
        self.menuShowing = True
        self.mChange = True

        self.display = Display(pygame.surface.Surface((self.w, self.h)), self, True, alpha=75)
        self.createMenu(surface)
        self.input = Input()
        self.input.set(pygame.KEYDOWN, pygame.K_o, "overlay", self.toggleOverlay)
        self.input.set(pygame.KEYDOWN, pygame.K_t, "menu", self.menu.toggleEnabled)
        self.input.set(pygame.KEYDOWN, pygame.K_RETURN, "save", self._map.save)
        self.input.set(pygame.KEYDOWN, pygame.K_LCTRL, "start", self.startBlock)
        self.input.set(pygame.KEYDOWN, pygame.K_LSHIFT, "end", self.endBlock)

    def createMenu(self, surface):
        self.menu = Menu((0, (const.screenSize[1] - 2) * const.res), surface)
        color = MColor((255, 0, 0), (0, 0, 255))
        self.menu.addItem("save", (0, 0, 32, 32), color, color, MText("Save"),
                          MAction(self.handleMenu, "save"))
        self.menu.addItem("pen", (32, 0, 32, 32), color, MText("Pen"), MToggle(False), MGroup(0),
                          MAction(self.handleMenu, "pen"))
        self.menu.addItem("box", (64, 0, 32, 32), color, MText("Box"), MToggle(False), MGroup(0),
                          MAction(self.handleMenu, "box"))
        self.menu.addItem("tiles", (96, 0, 32, 32), color, MText("Tiles"), MToggle(False), MGroup(1),
                          MAction(self.handleMenu, "tiles"))
        self.menu.addItem("wall", (196, 0, 32, 32), color, MText("W"), MToggle(False), MGroup(1),
                          MAction(self.handleMenu, "wall"))
        self.menu.addItem("empty", (228, 0, 32, 32), color, MText("V"), MToggle(False), MGroup(1),
                          MAction(self.handleMenu, "empty"))
        self.menu.addItem("death", (260, 0, 32, 32), color, MText("D"), MToggle(False), MGroup(1),
                          MAction(self.handleMenu, "death"))
        self.menu.addItem("start", (292, 0, 32, 32), color, MText("S"), MToggle(False), MGroup(1),
                          MAction(self.handleMenu, "start"))
        self.menu.addItem("end", (324, 0, 32, 32), color, MText("E"), MToggle(False), MGroup(1),
                          MAction(self.handleMenu, "end"))
        self.menu.addItem("collision", (500, 0, 100, 32), color, MText("Coll"), MToggle(False),
                          MAction(self.toggleOverlay))
        ts = self._map.getTileset()
        for i in range(const.TILE_SET_LENGTH):
            surf = pygame.surface.Surface((30, 30))
            surf.blit(ts, pygame.Rect(-1, -i * const.res, const.res - 2, const.res - 2))
            self.menu.addItem(i, (32 * i, 32, 32, 32), MImage(surf), MToggle(False), MGroup(2),
                              MAction(self.handleMenu, i))

    def pen(self, x, y, camera):
        block = None
        tile = (int((x + camera.x) / const.res),
                int((y + camera.y) / const.res))

        try:
            block = self._map.get(tile[0], tile[1])
        except:
            print("Unable to set tile {}.", tile)
        else:
            if self.bType == -1:
                block.setTile(self.brush)
            elif self.bType >= 0:
                block.setType(self.bType)
                self._delta.append(tile)

    def box(self, x, y, key):
        if not hasattr(self, "gen"):
            self.gen = 1
        for event, keyy in input:
            if event == pygame.MOUSEBUTTONDOWN:
                self.gen = {-1: 1, 1: -1}[self.gen]

    def toggleOverlay(self):
        self.menuShowing = not self.menuShowing

    def startBlock(self):
        self.modifier = 1

    def endBlock(self):
        self.modifier = 2

    def handleMouse(self, event, input):
        return {pygame.MOUSEBUTTONDOWN: True, pygame.MOUSEBUTTONUP: False}.get(event)

    def handleMenu(self, action):
        self.modifier = 0
        if "pen" == action:
            self.tool = 0
        if "box" == action:
            self.tool = 1
        if "tiles" == action:
            self.bType = -1

        if "empty" == action:
            self.bType = 0
        if "death" == action:
            self.bType = 4
        if "wall" == action:
            #self.menu.items[4].update(OColor=((0, 0, 255)))
            self.bType = 1
        if self.modifier == 1:
            #self.menu.items[4].update(OColor=((0, 255, 0)))
            self.bType = 2
        if self.modifier == 2:
            #self.menu.items[4].update(OColor=((255, 0, 255)))
            self.bType = 3

        if "save" == action:
            self._map.save()
        if "collision" == action:
            self.menuShowing = not self.menuShowing

        for i in range(const.TILE_SET_LENGTH):
            if i == action:
                self.brush = i

    def edit(self, inputs, camera):
        x, y = pygame.mouse.get_pos()  # fix it, it doesnt need this because "inputs" already has the mouse pos
        self.menu.tick(inputs, (x, y))

        self.input(inputs)

        for event, key in inputs:
            if not (event == pygame.KEYDOWN or event == pygame.KEYUP):
                self.painting = self.handleMouse(event, key)

        if self.painting:
            self.mChange = True
            if self.tool == 0:
                self.pen(x, y, camera)
            elif self.tool == 1:
                self.box(inputs, x, y)

    def update(self):
        tile = pygame.surface.Surface((const.res, const.res))
        for i, e in self._delta:
            colorKey = {Tile.Empty: (0, 0, 0),
                        Tile.Solid: (0, 0, 255),
                        Tile.Start: (0, 255, 0),
                        Tile.End: (255, 0, 255),
                        Tile.Deadly: (255, 0, 0)}[self._map.get(i, e).getType()]
            tile.fill(colorKey)
            self.display.update(tile, (i * const.res, e * const.res))
        self._delta = []

    def draw(self, surface, camera):
        if self._delta:
            self.update()
        if self.menuShowing:
            self.display.draw(surface, camera)

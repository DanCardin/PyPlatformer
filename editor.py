import pygame
import const
from display import Display
from enableable import Enableable
from object import Object
from menu import Menu, MText, MToggle, MAction, MGroup, MImage, MColor
from input import Input
from wall import Tiles


class Brush(object):
    def __init__(self, typ):
        self._typ = typ

    def apply(self, block):
        raise NotImplementedError()


class TileBrush(Brush):
    def apply(self, block):
        block.setTile(self._typ)


class WallBrush(Brush):
    def apply(self, block):
        block.setType(self.bType)


class Tool(object):
    def _getBlock(self, x, y):
        try:
            block = self._map.get(x, y)
        except:
            print("Unable to set tile ({}, {}).", x, y)
        else:
            self._apply(block, x, y)

    def _getBlocks(self, x, y):
        raise NotImplementedError()

    def apply(self, x, y):
        raise NotImplementedError()


class PenTool(Tool):
    def apply(self, x, y):
        self.brush.apply(self._getBlock(x, y))


class Editor(Object, Enableable):
    def __init__(self, map, surface):
        Object.__init__(self, (map.w, map.h + const.res))
        Enableable.__init__(self, False)

        self._map = map
        self._delta = [(i, e) for e in range(self._map.getSize(y=True))
                       for i in range(self._map.getSize(x=True))]

        self._brush = None
        self._tool = None
        self.painting = False
        self.menuShowing = True
        self.mChange = True
        self._applicable = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]

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
                          MAction(self._map.save))
        self.menu.addItem("pen", (32, 0, 32, 32), color, MText("Pen"), MToggle(), MGroup(0),
                          MAction(self.handleMenu, "pen"))
        self.menu.addItem("box", (64, 0, 32, 32), color, MText("Box"), MToggle(), MGroup(0),
                          MAction(self.handleMenu, "box"))
        self.menu.addItem("tiles", (96, 0, 32, 32), color, MText("Tiles"), MToggle(), MGroup(1),
                          MAction(self.handleMenu, "tiles"))
        self.menu.addItem("wall", (196, 0, 32, 32), color, MText("W"), MToggle(), MGroup(1),
                          MAction(self._setBrush, WallBrush(Tiles.Solid)))
        self.menu.addItem("empty", (228, 0, 32, 32), color, MText("V"), MToggle(), MGroup(1),
                          MAction(self._setBrush, WallBrush(Tiles.Empty)))
        self.menu.addItem("death", (260, 0, 32, 32), color, MText("D"), MToggle(), MGroup(1),
                          MAction(self._setBrush, WallBrush(Tiles.Deadly)))
        self.menu.addItem("start", (292, 0, 32, 32), color, MText("S"), MToggle(), MGroup(1),
                          MAction(self._setBrush, WallBrush(Tiles.Start)))
        self.menu.addItem("end", (324, 0, 32, 32), color, MText("E"), MToggle(), MGroup(1),
                          MAction(self._setBrush, WallBrush(Tiles.End)))
        self.menu.addItem("collision", (500, 0, 100, 32), color, MText("Coll"), MToggle(),
                          MAction(self.toggleOverlay))
        ts = self._map.getTileset()
        for i in range(const.TILE_SET_LENGTH):
            surf = ts.subsurface((0, i * const.res, 32, 32))
            self.menu.addItem(i, (32 * i, 32, 32, 32), MImage(surf), MToggle(), MGroup(2),
                              MAction(self._setBrush, TileBrush(i)))

    def pen(self, x, y, camera):
        block = None
        tile = (int((camera.x + x) / const.res),
                int((camera.y + y) / const.res))

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

    def _setBrush(self, brush):
        self._brush = brush

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
            self.bType = 1
        if self.modifier == 1:
            self.bType = 2
        if self.modifier == 2:
            self.bType = 3

        if "collision" == action:
            self.menuShowing = not self.menuShowing

        for i in range(const.TILE_SET_LENGTH):
            if i == action:
                self.brush = i

    def edit(self, inputs, camera):
        self.input(inputs)

        inputs = self.menu.tick([i for i in inputs if i.type in self._applicable])
        for event in inputs:
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                self.painting = True if event.type == pygame.MOUSEBUTTONDOWN else False

            if self.painting:
                self.mChange = True
                if self.tool == 0:
                    self.pen(event.pos[0], event.pos[1], camera)
                elif self.tool == 1:
                    self.box(inputs, event.pos[0], event.pos[1])

    def update(self):
        tile = pygame.surface.Surface((const.res, const.res))
        for i, e in self._delta:
            colorKey = {Tiles.Empty: (0, 0, 0),
                        Tiles.Solid: (0, 0, 255),
                        Tiles.Start: (0, 255, 0),
                        Tiles.End: (255, 0, 255),
                        Tiles.Deadly: (255, 0, 0)}[self._map.get(i, e).getType()]
            tile.fill(colorKey)
            self.display.update(tile, (i * const.res, e * const.res))
        self._delta = []

    def draw(self, surface, camera):
        if self._delta:
            self.update()
        if self.menuShowing:
            self.display.draw(surface, camera)

import pygame
import const
from display import Display
from enableable import Enableable
from object import Object
from menu import Menu, MText, MToggle, MAction, MGroup, MImage
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
        # a = MAction(self.handleMenu(None))
        self.menu.addItem("save", (0, 0, 32, 32), MText("Save"))
        self.menu.addItem("pen", (32, 0, 32, 32), MText("Pen"), MToggle(True), MGroup(0))
        self.menu.addItem("box", (64, 0, 32, 32), MText("Box"), MToggle(True), MGroup(0))
        self.menu.addItem("tiles", (96, 0, 32, 32), MText("Tiles"), MToggle(True), MGroup(1))
        self.menu.addItem("wall", (196, 0, 32, 32), MText("W"), MToggle(True), MGroup(1))
        self.menu.addItem("empty", (228, 0, 32, 32), MText("V"), MToggle(True), MGroup(1))
        self.menu.addItem("death", (260, 0, 32, 32), MText("D"), MToggle(True), MGroup(1))
        self.menu.addItem("start", (292, 0, 32, 32), MText("S"), MToggle(True), MGroup(1))
        self.menu.addItem("end", (324, 0, 32, 32), MText("E"), MToggle(True), MGroup(1))
        self.menu.addItem("collision", (500, 0, 100, 32), MText("Coll"), MToggle(True), MGroup(3))
        ts = self._map.getTileset()
        for i in range(const.TILE_SET_LENGTH):
            surf = pygame.surface.Surface((30, 30))
            surf.blit(ts, pygame.Rect(-1, -i * const.res, const.res - 2, const.res - 2))
            self.menu.addItem(i, (32 * i, 32, 32, 32), MImage(surf), MToggle(True), MGroup(2))

    def pen(self, key, camera):
        block = None
        tile = (int((key[0] + camera.x) / const.res),
                int((key[1] + camera.y) / const.res))

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

    def box(self, input, key):
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
            self._map.save()
        if "collision" in action:
            self.menuShowing = not self.menuShowing

        for i in range(const.TILE_SET_LENGTH):
            if i in action:
                self.brush = i

    def edit(self, inputs, camera):
        mPos = pygame.mouse.get_pos()  # fix it, it doesnt need this because "inputs" already has the mouse pos
        self.handleMenu(self.menu.tick(inputs, mPos), inputs)
        if self.painting:
            self.mChange = True
            if self.tool == 0:
                self.pen(mPos, camera)
            elif self.tool == 1:
                self.box(inputs, mPos)

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

import pygame
import const
from display import Display
from enableable import Enableable
from input import Input
from menu import Menu, MText, MToggle, MAction, MGroup, MImage, MColor
from object import Object
from showable import Showable
from wall import Tiles


class Brush(object):
    def __init__(self, brush):
        self._brush = brush

    def __call__(self, block):
        raise NotImplementedError()


class TileBrush(Brush):
    def __call__(self, block):
        block.setTile(self._brush)


class WallBrush(Brush):
    def __call__(self, block):
        block.setType(self._brush)


class Tool(object):
    def __init__(self, map):
        self._map = map

    def _getBlock(self, x, y):
        try:
            return self._map.get(x, y)
        except:
            print("Unable to get tile ({}, {}).", x, y)

    def _getBlocks(self, x, y):
        raise NotImplementedError()

    def __call__(self, x, y, brush):
        raise NotImplementedError()


class PenTool(Tool):
    def __call__(self, x, y, brush):
        block = self._getBlock(x, y)
        if block:
            brush(block)
            return [block]


class BoxTool(Tool):
    def __call__(self, x, y, brush):
        pass


class Editor(Enableable, Showable):
    def __init__(self, map, surface):
        Enableable.__init__(self, False)
        Showable.__init__(self, True)

        self._map = map
        self._delta = [tile for tile in self._map.getMap().values()]

        self._brush = None
        self._tool = None
        self._painting = False

        surf = pygame.surface.Surface((map.w, map.h))
        self._display = Display(surf, surf.get_rect(), True, alpha=75)
        self._createMenu(surface)

        self._input = Input()
        self._input.set(pygame.KEYDOWN, pygame.K_o, "overlay", self.toggleShowing)
        self._input.set(pygame.KEYDOWN, pygame.K_t, "menu", self.menu.toggleEnabled)
        self._input.set(pygame.KEYDOWN, pygame.K_RETURN, "save", self._map.save)

    def _createMenu(self, surface):
        self.menu = Menu((0, (const.screenSize[1] - 2) * const.res), surface)
        color = MColor((255, 0, 0), (0, 0, 255))
        self.menu.addItem("save", (0, 0, 32, 32), color, color, MText("Save"),
                          MAction(self._map.save))

        def _setTool(tool):
            self._tool = tool

        def _setBrush(brush):
            self._brush = brush

        self.menu.addItem("pen", (32, 0, 32, 32), color, MText("Pen"), MToggle(), MGroup(0),
                          MAction(_setTool, PenTool(self._map)))
        self.menu.addItem("box", (64, 0, 32, 32), color, MText("Box"), MToggle(), MGroup(0),
                          MAction(_setTool, BoxTool(self._map)))
        self.menu.addItem("wall", (196, 0, 32, 32), color, MText("W"), MToggle(), MGroup(1),
                          MAction(_setBrush, WallBrush(Tiles.Solid)))
        self.menu.addItem("empty", (228, 0, 32, 32), color, MText("V"), MToggle(), MGroup(1),
                          MAction(_setBrush, WallBrush(Tiles.Empty)))
        self.menu.addItem("death", (260, 0, 32, 32), color, MText("D"), MToggle(), MGroup(1),
                          MAction(_setBrush, WallBrush(Tiles.Deadly)))
        self.menu.addItem("start", (292, 0, 32, 32), color, MText("S"), MToggle(), MGroup(1),
                          MAction(_setBrush, WallBrush(Tiles.Start)))
        self.menu.addItem("end", (324, 0, 32, 32), color, MText("E"), MToggle(), MGroup(1),
                          MAction(_setBrush, WallBrush(Tiles.End)))
        self.menu.addItem("collision", (500, 0, 100, 32), color, MText("Coll"), MToggle(),
                          MAction(self.toggleShowing))
        ts = self._map.getTileset()
        for i in range(const.TILE_SET_LENGTH):
            surf = ts.subsurface((0, i * const.res, 32, 32))
            self.menu.addItem(i, (32 * i, 32, 32, 32), MImage(surf), MToggle(), MGroup(2),
                              MAction(_setBrush, TileBrush(i)))

    def tick(self, inputs, camera):
        self._input(inputs)
        inputs = self.menu.tick(inputs)

        for event in inputs:
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                    self._painting = True if event.type == pygame.MOUSEBUTTONDOWN else False

                if self._painting and self._tool and self._brush:
                    x, y = (int((event.pos[0] + camera.x) / const.res),
                            int((event.pos[1] + camera.y) / const.res))
                    blocks = self._tool(x, y, self._brush)
                    if blocks:
                        self._delta.extend(blocks)

    def update(self):
        surf = pygame.surface.Surface((const.res, const.res))
        for tile in self._delta:
            surf.fill({Tiles.Empty: (0, 0, 0),
                       Tiles.Solid: (0, 0, 255),
                       Tiles.Start: (0, 255, 0),
                       Tiles.End: (255, 0, 255),
                       Tiles.Deadly: (255, 0, 0)}[tile.getType()])
            self._display.update(surf, tile)
        self._delta = []

    def draw(self, surface, camera):
        if self._delta:
            self.update()
        if self.showing():
            self._display.draw(surface, camera)

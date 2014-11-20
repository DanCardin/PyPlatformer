import pygame
import const
from display import Display
from enableable import Enableable
from input import Input
from menu import Menu, MText, MAction, MImage, MColor, MAlpha, MenuItem
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
        self._brush = None
        self._tool = None
        self._painting = False

        surf = pygame.surface.Surface((map.w, map.h))
        self._display = Display(surf, surf.get_rect(), True, alpha=75)
        for tile in self._map.getMap().values():
            tile.subscribe("editor", self._update)

        self._createMenu(surface)

        self._input = Input()
        self._input.set(pygame.KEYDOWN, pygame.K_o, "overlay", self.toggleShowing)
        self._input.set(pygame.KEYDOWN, pygame.K_t, "menu", self.menu.toggleEnabled)
        self._input.set(pygame.KEYDOWN, pygame.K_RETURN, "save", self._map.save)

    def _createMenu(self, surface):
        self.menu = Menu((0, (const.screenSize[1] - 2) * const.res), surface)

        def _setTool(tool):
            self._tool = tool

        def _setBrush(brush):
            self._brush = brush

        color = MColor((255, 0, 0), (0, 0, 255))
        alpha = MAlpha(200)
        self.menu.addItem("save", (450, 0, 49, 32), color, alpha, MText("Save"),
                          MAction(self._map.save))
        self.menu.addGroup("collision",
                           MenuItem((500, 0, 49, 32), color, alpha, MText("Coll"),
                                    MAction(self.toggleShowing)))

        self.menu.addGroup("Tools",
            MenuItem((0, 0, 31, 32), color, alpha, MText("Pen"),
                     MAction(_setTool, PenTool(self._map))),
            MenuItem((32, 0, 31, 32), color, alpha, MText("Box"),
                     MAction(_setTool, BoxTool(self._map))))

        self.menu.addGroup("Brushes",
            MenuItem((196, 0, 31, 32), color, alpha, MText("W"),
                     MAction(_setBrush, WallBrush(Tiles.Solid))),
            MenuItem((228, 0, 31, 32), color, alpha, MText("V"),
                     MAction(_setBrush, WallBrush(Tiles.Empty))),
            MenuItem((260, 0, 31, 32), color, alpha, MText("D"),
                     MAction(_setBrush, WallBrush(Tiles.Deadly))),
            MenuItem((292, 0, 31, 32), color, alpha, MText("S"),
                     MAction(_setBrush, WallBrush(Tiles.Start))),
            MenuItem((324, 0, 31, 32), color, alpha, MText("E"),
                     MAction(_setBrush, WallBrush(Tiles.End))))

        ts = self._map.getTileset()
        for i in range(const.TILE_SET_LENGTH):
            surf = ts.subsurface((0, i * const.res, 32, 32))
            self.menu.appendGroup("Brushes",
                MenuItem((32 * i, 32, 32, 32), MImage(surf), alpha,
                              MAction(_setBrush, TileBrush(i))))

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

    def _update(self, block):
        surf = pygame.surface.Surface((const.res, const.res))
        surf.fill({Tiles.Empty: (0, 0, 0),
                   Tiles.Solid: (0, 0, 255),
                   Tiles.Start: (0, 255, 0),
                   Tiles.End: (255, 0, 255),
                   Tiles.Deadly: (255, 0, 0)}[block.getType()])
        self._display.update(surf, block)

    def draw(self, surface, camera):
        if self.showing():
            self._display.draw(surface, camera)

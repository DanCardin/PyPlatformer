import pygame
import const
from display import Display
from enableable import Enableable
from input import Input
from menu import Menu, MText, MAction, MImage, MColor, MAlpha, MenuItem
from surface import Surface
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


class SpawnBrush(Brush):
    def __call__(self, block):
        block.setType(Tiles.EnemySpawn)
        block.setAttr("spawnNum", self._brush)


class Tool(object):
    def __init__(self, map):
        self._map = map

    def _getBlock(self, x, y):
        try:
            return self._map.get(x, y)
        except:
            print("Unable to get tile ({}, {}).", x, y)

    def _getRelPos(self, x, y):
        return x // const.res, y // const.res

    def _getBlocks(self, x, y):
        raise NotImplementedError()

    def __call__(self, x, y, brush, painting):
        raise NotImplementedError()


class PenTool(Tool):
    def __call__(self, x, y, brush, painting):
        if brush:
            block = self._getBlock(*self._getRelPos(x, y))
            if block:
                brush(block)
                return [block]


class ModifyTool(Tool):
    def __init__(self, map):
        super().__init__(map)
        self._lastPainting = None
        self._block = None

    def __call__(self, x, y, brush, painting):
        if self._lastPainting is not painting:
            self._lastPainting = painting
            self._block = self._getBlock(*self._getRelPos(x, y))
        if self._block:
            self._block.h = min(32, max(1, y - self._block.y))
            return [self._block]


class BoxTool(Tool):
    def __call__(self, x, y, dx, dy, brush):
        pass


class Paint(object):
    pass


class Editor(Enableable, Showable):
    def __init__(self, map, surface):
        Enableable.__init__(self, False)
        Showable.__init__(self, True)

        self._map = map
        self._tool = None
        self._brush = None
        self._painting = None

        surf = Surface((map.w, map.h))
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
        self.menu.addGroup("Collision",
                           MenuItem((500, 0, 49, 32), color, alpha, MText("Coll"),
                                    MAction(self.toggleShowing)))

        self.menu.addGroup("Tools",
            MenuItem((0, 0, 40, 32), color, alpha, MText("Pen"),
                     MAction(_setTool, PenTool(self._map))),
            MenuItem((41, 0, 40, 32), color, alpha, MText("Mod"),
                     MAction(_setTool, ModifyTool(self._map))))

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

        spawnBrush = MenuItem((370, 0, 31, 32), color, alpha, MText("*"),
                              MAction(_setBrush, SpawnBrush(1)))
        self.__spawnBrushCount = 1
        def newSpawn(diff):
            self.__spawnBrushCount += diff
            brush = SpawnBrush(self.__spawnBrushCount)
            spawnBrush.update(MAction(_setBrush, brush))
            if isinstance(self._brush, SpawnBrush):
                self._brush = brush

        self.menu.appendGroup("Brushes", spawnBrush)
        self.menu.addItem("upSpawn", (402, 0, 31, 16), color, alpha, MText("+"),
                          MAction(newSpawn, 1))
        self.menu.addItem("downSpawn", (402, 17, 31, 15), color, alpha, MText("-"),
                          MAction(newSpawn, -1))

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
                    if self._painting and event.type == pygame.MOUSEBUTTONUP:
                        self._painting = None
                    elif not self._painting and event.type == pygame.MOUSEBUTTONDOWN:
                        self._painting = Paint()

                if self._painting and self._tool:
                    x, y = event.pos[0] + camera.x, event.pos[1] + camera.y
                    self._tool(x, y, self._brush, self._painting)

    def _update(self, block):
        surf = Surface((const.res, const.res))
        fill = {Tiles.Empty: (0, 0, 0),
                Tiles.Solid: (0, 0, 255),
                Tiles.Start: (0, 255, 0),
                Tiles.End: (255, 0, 255),
                Tiles.Deadly: (255, 0, 0),
                Tiles.EnemySpawn: (0, 255, 255)}[block.getType()]
        pygame.draw.rect(surf, fill, (block.relX, block.relY, block.w, block.h))
        pygame.draw.rect(surf, (255, 255, 255), (block.relX, block.relY, block.w, block.h), 1)

        isSpawn = block.getAttr("spawnNum")
        if isSpawn:
            text = pygame.font.SysFont("arial", 25).render(str(isSpawn), 1, (0, 0, 0))
            surf.blit(text, (int(surf.get_width() / 2 - text.get_width() / 2),
                             int(surf.get_height() / 2 - text.get_height() / 2)))
        self._display.update(surf, block)

    def draw(self, surface, camera):
        if self.showing():
            self._display.draw(surface, camera)

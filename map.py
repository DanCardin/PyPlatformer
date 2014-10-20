import pygame
import re
import const

from object import Object
from files import Files
from wall import Wall
from display import Display
from wall import Tile


class Map(Object):
    def __init__(self, file, tileset, resolution):
        Object.__init__(self)
        self._map = {}
        self._tiles = {}
        self._mapDelta = []
        self._wx = 0
        self._hy = 0
        self.display = None

        self._file = file
        self._scale = const.res / resolution
        self._tileset = pygame.transform.scale(Files().loadImage(tileset),
                            (const.res, const.res * const.TILE_SET_LENGTH)).convert()
        transColor = self._tileset.get_at((0, 0))
        self._tileset.set_colorkey(transColor)

    def getStart(self):
        return self._tiles[Tile.Start][0]

    def getTileset(self):
        return self._tileset

    def getScale(self):
        return self._scale

    def getSize(self, x=None, y=None):
        if x and y:
            return (self._wx, self._hy)
        if x:
            return self._wx
        if y:
            return self._hy

    def get(self, x, y):
        return self._map[(x, y)]

    def set(self, x, y, to):
        self._map[(x, y)] = to

    def load(self):
        file = Files().openFile(self._file)
        match = re.search("^\((\d+),(\d+)\)", file)
        self._wx = int(match.group(1))
        self._hy = int(match.group(2))
        self.w = self._wx * const.res
        self.h = self._hy * const.res

        tiles = re.findall("\((\d+),(\d+),(\d+),(\d+):(\d+),(\d+)\)", file)
        for i in range(self._wx):
            for e in range(self._hy):
                x, y, w, h, typ, tile = tiles[i * self._hy + e]
                x, y, w, h, typ, tile = int(x), int(y), int(w), int(h), int(typ), int(tile)
                wall = Wall((i * const.res + self._scale * x,
                             e * const.res + self._scale * y,
                             w * self._scale, h * self._scale), typ, tile)

                self._map[(i, e)] = wall
                self._tiles.setdefault(wall.getType(), []).append(wall)
                self._mapDelta.append(wall)

        self.display = Display(pygame.surface.Surface((self.w, self.h)), self, True)

    def save(self):
        s = ["(%s,%s)\n" % (int(const.res / self.const.res), self._wx, self._hy)]
        for i in range(self.size[1]):
            for e in range(self.size[0]):
                tile = self._map(None, i)
                rect = tile.rect
                s.append("(%s,%s,%s,%s:%s,%s)" % (rect.x, rect.y, rect.w, rect.h, tile.type, tile.tile).ljust(20))
            s.append("\n")
        Files().saveFile(''.join(s), self.file)

    def _updateMap(self):
        for block in self._mapDelta:
            self.display.update(self._tileset, (block.x, block.y),
                                     (0, block.getTile() * const.res, const.res, const.res))
        self._mapDelta = []

    def draw(self, surface, camera):
        if self._mapDelta:
            self._updateMap()
        self.display.draw(surface, camera)

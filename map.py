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
        self.display = None

        self._file = file
        self._scale = const.res / resolution
        self.tileset = Files().loadImage(tileset)
        self.tileset = pygame.transform.scale(Files().loadImage(tileset),
                            (const.res, const.res * const.TILE_SET_LENGTH)).convert()


    def __call__(self, x=None, y=None):
        if x is None and y is None:
            return self._map

        if x is None:
            result = []
            for i in range(self.size[0] - 1):
                result.append(map[(i, y)])
            return result

        if y is None:
            result = []
            for i in range(self.size[1] - 1):
                result.append(map[(x, i)])
            return result

        return self._map[(x, y)]

    def getStart(self):
        return self._tiles[2][0]

    def getScale(self):
        return self._scale

    def get(self, x, y):
        return self._map[(x, y)]

    def load(self):
        file = Files().openFile(self._file)
        match = re.search("^\((\d+),(\d+)\)", file)
        self.x = int(match.group(1))
        self.y = int(match.group(2))
        self.w = self.x * const.res
        self.h = self.y * const.res

        search = "\((\d+),(\d+),(\d+),(\d+),(\d+),(\d+),\)"
        tiles = re.findall(search, file)
        for i in range(self.x):
            for e in range(self.y):
                x, y, w, h, type, tile = tiles[i * self.y + e]
                wall = Wall((i * const.res + self._scale * int(x),
                             e * const.res + self._scale * int(y),
                            int(w) * self._scale, int(h) * self._scale),
                            int(type), int(tile))
                self._map[(i, e)] = wall
                self._tiles.setdefault(int(type), [])
                self._tiles[int(type)].append(wall)
                if wall.getType() == Tile.Start:
                    self._start = (wall.x, wall.y)

                self._mapDelta.append(wall)

        self.display = Display(pygame.surface.Surface((self.w, self.h)), self, True)

    def save(self):
        s = ["(%s,%s)\n" % (int(const.res / self.const.res), self.x, self.y)]
        for i in range(self.size[1]):
            for e in range(self.size[0]):
                tile = self._map(None, i)
                rect = tile.rect
                s.append("(%s,%s,%s,%s:%s,%s)" % (rect.x, rect.y, rect.w, rect.h, tile.type, tile.tile).ljust(20))
            s.append("\n")
        Files().saveFile(''.join(s), self.file)

    def _updateMap(self):
        for block in self._mapDelta:
            self.display.updateImage(self.tileset, (block.x, block.y),
                                     (0, block.getTile() * const.res, const.res, const.res))
        self._mapDelta = []

    def draw(self, surface, camera):
        if self._mapDelta:
            self._updateMap()
        self.display.draw(surface, camera)

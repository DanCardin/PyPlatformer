import pygame
import re
import const

from object import Object
from files import Files
from wall import Wall
from display import Display
from wall import Tiles


class Map(Object):
    def __init__(self, file, tileset):
        Object.__init__(self)
        self._map = {}
        self._tiles = {}
        self._wx = 0
        self._hy = 0
        self.display = None

        self._file = file
        self._tileset = Files().loadImage(tileset)
        self._tileset.set_colorkey(self._tileset.get_at((0, 0)))

    def getStart(self):
        return self._tiles[Tiles.Start][0]

    def getTileset(self):
        return self._tileset

    def getSize(self, x=None, y=None):
        if x and y:
            return (self._wx, self._hy)
        if x:
            return self._wx
        if y:
            return self._hy

    def getMap(self):
        return self._map

    def inRange(self, x, y):
        mx, my = self.getSize(x=True, y=True)
        return max(0, min(mx, x)), max(0, min(my, y))

    def get(self, x, y):
        return self._map[self.inRange(x, y)]

    def set(self, x, y, to):
        self._map[self.inRange(x, y)] = to

    def load(self):
        file = Files().openFile(self._file)
        match = re.search("^\((\d+),(\d+)\)", file)
        self._wx = int(match.group(1))
        self._hy = int(match.group(2))
        self.w = self._wx * const.res
        self.h = self._hy * const.res
        self.display = Display(pygame.surface.Surface((self.w, self.h)), self, True)

        tiles = re.findall("\((\d+),(\d+),(\d+),(\d+):(\d+),(\d+)\)", file)
        for i in range(self._hy):
            for e in range(self._wx):
                x, y, w, h, typ, tile = tiles[i * self._wx + e]
                x, y, w, h, typ, tile = int(x), int(y), int(w), int(h), int(typ), int(tile)
                wall = Wall((x, y, w, h), typ, tile)
                wall.subscribe(self._updateMap)

                self._map[(e, i)] = wall
                self._tiles.setdefault(wall.getType(), []).append(wall)

    def save(self):
        s = ["(%s,%s)\n" % (self._wx, self._hy)]
        for i in range(self._hy):
            for e in range(self._wx):
                tile = self._map[(e, i)]
                s.append("({},{},{},{}:{},{})".format(tile.x, tile.y,
                                                      tile.w, tile.h,
                                                      tile.getType().value,
                                                      tile.getTile()).ljust(20))
            s.append("\n")
        Files().saveFile(''.join(s), self._file)

    def _updateMap(self, block):
        self.display.update(self._tileset, (block.x, block.y),
                            (0, block.getTile() * const.res, const.res, const.res))

    def draw(self, surface, camera):
        self.display.draw(surface, camera)

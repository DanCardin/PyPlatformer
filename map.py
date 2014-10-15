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

        self._file = file
        self._scale = const.res / resolution

        if tileset:
            self.tileset = Files().loadImage(tileset)

            self.mapDelta = []
            for i in self._map.keys():
                self.mapDelta.append(i)

            self.display = Display(self.tileset, self, self, False)
            # Display(self.acmap, Object((0, 0, 0, 0)), self.acmap.get_rect(), False)
# class Map(object):
#     def __init__(self, File, Tileset, res):
#         self.tileset = pygame.transform.scale(self.fileMod.loadImage(Tileset), (res, res * TILE_SET_LENGTH)).convert()
#         self.transColor = self.tileset.get_at((0, 0))
#         self.acmap = pygame.surface.Surface((self.size[0] * res, self.size[1] * res))
#         self.acmap.set_colorkey(self.transColor)
#         self.mChange = True
#         self.display = Display(self.acmap, Object((0, 0, 0, 0)), self.acmap.get_rect(), False)

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
        print(self._tiles[2][0])
        return self._tiles[2][0]

    def getScale(self):
        return self._scale

    def getType(self, x, y):
        return self._map[(x, y)].type

    def setType(self, x, y, type):
        self._map[(x, y)].type = type

    def getTile(self, x, y):
        return self._map[(x, y)].tile

    def setTile(self, x, y, tile):
        self._map[(x, y)].tile = tile

    def wallDim(self, x, y):
        return Object((x * const.res + self._map[(x, y)].x,
                      y * const.res + self._map[(x, y)].y,
                      self._map[(x, y)].w,
                      self._map[(x, y)].h))

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
                if wall.type == Tile.Start:
                    self._start = (i * const.res + 32, e * const.res - 48)

    def save(self):
        s = ["(%s,%s)\n" % (int(const.res / self.const.res), self.x, self.y)]
        for i in range(self.size[1]):
            for e in range(self.size[0]):
                tile = self._map(None, i)
                rect = tile.rect
                s.append("(%s,%s,%s,%s:%s,%s)" % (rect.x, rect.y, rect.w, rect.h, tile.type, tile.tile).ljust(20))
            s.append("\n")
        Files().saveFile(''.join(s), self.file)

    def initDrawMap(self):
        for i, e in self.mapDelta:
            self.display.image.blit(self.tileset,
                                    (i * const.res, e * const.res),
                                    (0, self._map[(i, e)].tile * const.res, const.res, const.res))

    def draw(self, surface, camera):
        if self.mapDelta:
            self.initDrawMap()
            self.mapDelta = []
        self.display.draw(surface, camera)

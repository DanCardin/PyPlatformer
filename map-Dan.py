# import const
# import re

# from object import *
# from main import *
# from files import *
# from wall import *
# from display import *

# class Map(Object):
#     def __init__(self, File, Tileset):
#         Object.__init__(self)
#         self._map = {}
#         self.load(File)

#         if Tileset:
#             self.tileset = Files().loadImage(Tileset[0], Tileset[1])

#             self.mapDelta = []
#             for i in self._map.keys():
#                 self.mapDelta.append(i)

#             self.display = Display(self, None, Tileset[1])

#     def __call__(self, x=None, y=None):
#         if x is None and y is None:
#             return self._map

#         if x is None:
#             result = []
#             for i in range(self.size[0] - 1):
#                 result.append(map[(i, y)])
#             return result

#         if y is None:
#             result = []
#             for i in range(self.size[1] - 1):
#                 result.append(map[(x, i)])
#             return result

#         return self._map[(x, y)]

#     def load(self, filename):
#         file = Files().openFile(filename)
#         print(file[:20])
#         match = re.search("^\((.+),(.+)\)", file)
#         self.x = int(match.group(1))
#         self.y = int(match.group(2))
#         self.w = self.x * const.res
#         self.h = self.y * const.res

#         search = "\((\d+),(\d+),(\d+),(\d+):(\d+),(\d+)\)"
#         tiles = re.findall(search, file)
#         for i in range(self.x):
#             for e in range(self.y):
#                 tile = tiles[i * self.x + e]
#                 self._map[(i, e)] = Wall((i * const.res + int(tile[0]), e * const.res +
#                     int(tile[1]), int(tile[2]) * const.res, int(tile[3]) * const.res),
#                     int(tile[4]), int(tile[5]))

#     def save(self):
#         s = ["(%s,%s)\n" % (int(const.res / self.const.res), self.x, self.y)]
#         for i in range(self.size[1]):
#             for e in range(self.size[0]):
#                 tile = self._map(None, i)
#                 rect = tile.rect
#                 s.append("(%s,%s,%s,%s:%s,%s)" % (rect.x, rect.y, rect.w, rect.h, tile.type, tile.tile).ljust(20))
#             s.append("\n")
#         Files().saveFile(''.join(s), self.file)

#     def initDrawMap(self):
#         for i, e in self.mapDelta:
#             self.display.image.blit(self.tileset, (i * const.res, e * const.res), (0, self._map[(i, e)].tile * const.res, const.res, const.res))

#     def draw(self, surface, camera):
#         if self.mapDelta:
#             self.initDrawMap()
#             self.mapDelta = []
#         self.display(surface, camera, camera)


import pygame
from const import *
from files import *
from wall import *
from display import *


class Map(object):
    def __init__(self, File, Tileset):
        self.fileMod = Files()
        self.size = ()
        self.res = 0
        self.__map = [[]]
        self.start = ()
        self.file = File
        self.tileset = pygame.transform.scale(self.fileMod.loadImage(Tileset), (res, res * TILE_SET_LENGTH)).convert()
        self.load(self.file)
        self.transColor = self.tileset.get_at((0, 0))
        self.acmap = pygame.surface.Surface((self.size[0] * res, self.size[1] * res))
        self.acmap.set_colorkey(self.transColor)
        self.mChange = True
        self.display = Display(self.acmap, Object((0, 0, 0, 0)), self.acmap.get_rect(), False)

    def load(self, filename):
        pos, walls, bg = [], [], []
        s = self.fileMod.openFile(filename)
        for i in range(3):
            poss = s.find(".")
            bg.append(int(s[:poss]))
            s = s[poss + 1:]
        tot, s = float(res) / float(bg[0]), s[1:]
        for i in range(bg[1]):
            walls.append([])
            for e in range(bg[2]):
                end = s.find(")")
                ns, s, pos = s[:end], s[end + 2:], []
                while len(ns) > 0:
                    com = ns.find(",")
                    pos.append(int(ns[:com]))
                    ns = ns[com + 1:]
                if pos[4] == 2:
                    star = (i * res, e * res)
                walls[i].append(Wall((pos[0] * tot, pos[1] * tot, pos[2] * tot, pos[3] * tot, pos[4], pos[5])))
        self.size, self.res, self.__map, self.start = (i + 1, e + 1), tot, walls, star

    def save(self):
        s = ["%s.%s.%s." % (int(res / self.res), self.size[0], self.size[1])]
        [[s.append("(%s,%s,%s,%s,%s,%s,)" % (e.x, e.y, int(e.w / self.res), int(e.h / self.res), e.type, e.tile)) for e in i] for i in self.__map]
        ns = ''.join(s)
        self.fileMod.saveFile(ns, self.file)

    def getType(self, x, y):
        return self.__map[x][y].type

    def setType(self, x, y, Type):
        self.__map[x][y].type = Type

    def getTile(self, x, y):
        return self.__map[x][y].tile

    def setTile(self, x, y, Tile):
        self.__map[x][y].tile = Tile

    def wallDim(self, x, y):
        return pygame.Rect(x * res + self.__map[x][y].x, y * res + self.__map[x][y].y, self.__map[x][y].w, self.__map[x][y].h)

    def initDrawMap(self):
        for i in range(self.size[0]):
            for e in range(self.size[1]):
                til = pygame.surface.Surface((res, res))
                til.blit(self.tileset, (0, -1 * self.__map[i][e].tile * res, res, res))
                self.acmap.blit(til, (i * res, e * res))

    def draw(self, surface, camera):
        if self.mChange:
            self.initDrawMap()
        self.display.draw(surface, camera)

import re
import const

from display import Display, Drawable
from files import Files
from object import Object
from surface import Surface
from wall import Wall


class Map(Object, Drawable):
    def __init__(self, file, tileset):
        super().__init__()

        self._file = file
        self._tileset = Files.loadImage(tileset)
        self._tileset.set_colorkey(self._tileset.get_at((0, 0)))

    def getType(self, typ):
        return self._tiles.get(typ, [])

    def getTileset(self):
        return self._tileset

    def getAttr(self, attr):
        result = self._attributes.get(attr)
        if result is None:
            raise ValueError("couldnt find attr: {}, valid attrs are: {}".format(attr, self._attributes.keys()))
        return result

    def getSize(self, x=None, y=None):
        if x and y:
            return (self.getAttr("w"), self.getAttr("h"))
        if x:
            return self.getAttr("w")
        if y:
            return self.getAttr("h")

    def getMap(self):
        return self._map

    def inRange(self, x, y):
        mx, my = self.getSize(x=True, y=True)
        return max(0, min(mx, x)), max(0, min(my, y))

    def get(self, x, y):
        return self._map[self.inRange(x, y)]

    def set(self, x, y, to):
        self._map[self.inRange(x, y)] = to

    def loadAttributes(self, attrName, data):
        strToClass = globals()['__builtins__']
        result = {}
        sectionMatch = r"^\s*{0}:\s*".format(attrName)
        attrSet = re.search(r"{0}\{{(.*?)\}}".format(sectionMatch), data, flags=(re.DOTALL | re.MULTILINE)).groups()[0]

        def do_nothing(input):
            return input.group()

        def capture_tuple(input):
            cast_str, key = input.groups()
            cast = strToClass[cast_str]
            return tuple(cast(i) for i in key.split(', ') if cast)

        attrMatches = [(r"(\w+)", do_nothing), (r"(\w*)\((\w+,\s*\w+)\)", capture_tuple)]
        total_line_match = r"^\s*(.*?):\s*\((\w+)\)(.*),$"

        singleKeyMatch = re.finditer(total_line_match, attrSet, flags=re.MULTILINE)
        for match in singleKeyMatch:
            for attrMatch, key_func in attrMatches:
                name, typ, value = match.groups()
                name_match = re.match(r"^{}$".format(attrMatch), name)
                if name_match:
                    result[key_func(name_match)] = strToClass[typ](value)
        return result

    @property
    def enemies(self):
        return self._enemies.copy()

    def load(self):
        self._map = {}
        self._tiles = {}
        self._attributes = {}

        file = Files.openFile(self._file)
        self._attributes = self.loadAttributes('attribs', file)
        self._enemies = self.loadAttributes('enemies', file)
        self.w = self.getAttr("w") * const.res
        self.h = self.getAttr("h") * const.res
        self._display = Display(Surface((self.w, self.h)), klass=self, transparent=True)

        file = re.search("map: {(.*?)}", file, flags=re.DOTALL).group(1)
        for tile in re.finditer(r"\((.*?):(.*?)\)", file):
            rect, right = tile.group(1), tile.group(2)
            rect = re.match(r"(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)", rect)
            if not rect:
                raise Exception("Unrecognized pattern: {}".format(rect))

            details = re.match(r"(\d+),(\d+)$", right)
            if not details:
                raise Exception("Unrecognized pattern: {}".format(right))

            i, e = int(rect.group(1)), int(rect.group(2))
            x, y, w, h = rect.group(3), rect.group(4), rect.group(5), rect.group(6)
            x, y, w, h = int(x), int(y), int(w), int(h)
            typ, tile = int(details.group(1)), int(details.group(2))

            attrib = {}
            wall = Wall((x, y, w, h), typ, tile, attrib)
            wall.subscribe("map", self._updateMap)

            self._map[(i, e)] = wall
            self._tiles.setdefault(wall.getType(), []).append(wall)

    def save(self):
        s = []

        s.append("attribs: {\n")
        for a, val in self._attributes.items():
            s.append("    {}: {},\n".format(a, val))
        s.append("}\n")

        s.append("map: {\n")
        for i in range(self.getAttr("h")):
            for e in range(self.getAttr("w")):
                tile = self._map[(e, i)]
                s.append("({},{},{},{},{},{}:{},{}".format(e, i,
                                                           tile.x, tile.y,
                                                           tile.w, tile.h,
                                                           tile.getType().value,
                                                           tile.getTile()))
                spawn = tile.getAttr("spawnNum")
                if spawn:
                    s.append(",[{}]".format(str(spawn)))
                s.append(")")
            s.append("\n")
        s.append("}")
        Files.saveFile(self._file, ''.join(s))

    def _updateMap(self, block):
        try:
            self._tiles.setdefault(block.getType(), []).remove(block)
        except ValueError:
            pass
        self._tiles.setdefault(block.getType(), []).append(block)
        self._display.update(Surface((const.res, const.res)), block)
        self._display.update(self._tileset,
                             Object(rect=(block.mapX * const.res, block.mapY * const.res,
                                          const.res, const.res)),
                             Object(rect=(0, block.getTile() * const.res, const.res, const.res)))

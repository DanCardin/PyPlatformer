import const

from pygame import KEYDOWN, K_e
from pygame.display import set_mode
from pygame.mixer import Sound
from pygame.surface import Surface

from background import Background
from camera import Camera
from display import Display
from editor import Editor
from input import Input
from map import Map
from mchar import MChar
from wall import Tile


class Level(object):
    def __init__(self, surface, level):
        self._surface = surface
        self._complete = False
        self.entityId = 0
        self.entities = {}
        self.registered = {}

        self.map = Map(level[0], level[1], level[2])
        self.input = Input()
        self.input.set(KEYDOWN, K_e, "editor", self.toggleEditor)

    def start(self):
        self.entities = {}
        self.map.load()
        self._total_surface = Surface((self.map.w, self.map.h))
        self.addEntity(register=True,
                       entity=MChar(self.map.getStart(), (20, 26),
                                    tuple([x * self.map.getScale() for x in const.playerSpeed]),
                                    const.playerTileset, True, self))
        self._camera = Camera(self._total_surface,
                              tuple([s * const.res for s in const.screenSize]),
                              (self.map.w, self.map.h),
                              (150, 200, 150, 200), self.get(0))
        self.background = Background(self._camera,
                                     const.backgrounds, self.map.getScale())
        self.editor = Editor(self.map, self._camera)
        self.sound = Sound("assets\\music.ogg")
        # self.sound.play(-1)

    def addEntity(self, register=False, id=None, entity=None):
        if not entity:
            raise Exception("Entity must not be None.")

        reg = self.registered if register else self.entities
        tid = self.entityId if not id else id

        reg[tid] = entity
        if not id:
            entity.id = self.entityId
            self.entityId += 1

    def removeEntity(self, entity):
        del self.entities[entity.id]

    def get(self, entityId):
        result = self.entities.get(entityId)
        if not result:
            result = self.registered.get(entityId)
        return result

    def isLevelComplete(self):
        return self._complete

    def process(self, input):
        for entity in self.registered.values():
            result = entity.tick(input)
            # if Tile.Start in result.values():
            #     self._complete = True

        for entity in self.entities.values():
            entity.tick([])

    def render(self):
        self.background.draw(self._total_surface, self._camera)
        for entities in [self.entities, self.registered]:
            for entity in entities.values():
                entity.draw(self._total_surface, self._camera)
        self.map.draw(self._total_surface, self._camera)
        if self.editor.enabled:
            self.editor.draw(self._total_surface, self._camera)

        self._camera.draw(self._surface)

    def toggleEditor(self):
        self.editor.enabled = not self.editor.enabled
        size = 2 if self.editor.enabled else 0
        self._surface = set_mode((const.screenSize[0] * const.res,
                                  const.screenSize[1] * const.res + size * const.res))

    def tick(self, inputs):
        self.input(inputs)
        self.process(inputs)
        self._camera.tick()
        self.background.tick()

        if self.editor.enabled:
            self.editor.edit(inputs)

        self.render()

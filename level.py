import pygame
import const
from map import Map
from background import Background
from camera import Camera
from editor import Editor
from input import Input
from mchar import MChar
from wall import Tile


class Level(object):
    def __init__(self, level):
        self._complete = False
        self.entityId = 0
        self.entities = {}
        self.registered = {}

        self.map = Map(level[0], level[1], level[2])
        self.input = Input()
        self.input.set(pygame.KEYDOWN, pygame.K_e, "editor", self.toggleEditor)

    def start(self):
        self.entities = {}
        self.map.load()
        self.addEntity(register=True,
                       entity=MChar(self.map.getStart(), (20, 26),
                                    tuple([x * self.map.getScale() for x in const.playerSpeed]),
                                    const.playerTileset, True, self))
        self.camera = Camera(tuple([s * const.res for s in const.screenSize]),
                             (150, 200, 150, 200), self.get(0),
                             (self.map.size[0] * const.res, self.map.size[1] * const.res))
        self.background = Background(self.camera, const.backgrounds, self.map.getScale())
        self.editor = Editor(self.map, self.camera)
        self.sound = pygame.mixer.Sound("assets\\music.ogg")
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

    def isComplete(self):
        return self._complete

    def process(self, input):
        for entity in self.registered.values():
            result = entity.tick(input)
            if Tile.End in result.keys():
                self._complete = True

        for entity in self.entities.values():
            entity.tick([])

    def render(self, surface):
        self.background.draw(surface, self.camera)
        for entities in [self.entities, self.registered]:
            for entity in entities.values():
                entity.display.draw(surface, self.camera)
                if hasattr(entity, "weapon"):
                    entity.weapon.draw(surface, self.camera)
        self.map.draw(surface, self.camera)
        if self.editor.enabled:
            self.editor.draw(surface, self.camera)

    def toggleEditor(self):
        global screen
        self.editor.enabled = not self.editor.enabled
        size = 2 if self.editor.enabled else 0
        screen = pygame.display.set_mode((const.screenSize[0] * const.res,
                                          const.screenSize[1] * const.res + size * const.res))

    def tick(self, inputs, surface):
        self.input(inputs)
        self.process(inputs)
        self.camera.tick()
        self.background.tick()

        if self.editor.enabled:
            self.editor.edit(inputs)

        self.render(surface)

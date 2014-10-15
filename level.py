import pygame
import const
from map import *
from background import Background
from camera import Camera
from editor import Editor
from input import Input
from mchar import MChar


class Level(object):
    def __init__(self, level):
        self.camera = None
        self.editor = None
        self.entities = {}
        self.entityId = 0

        self.map = Map(level[0], level[1], level[2])
        self.input = Input()
        self.input.set(pygame.KEYDOWN, pygame.K_e, "editor", self.toggleEditor)
        self.map.initDrawMap()

    def start(self):
        self.entities = {}
        start = self.map.getStart()
        self.addEntity(entity=MChar((start[0], start[1], 20, 26),
                             (const.playerSpeed[0] * const.res, const.playerSpeed[1] * const.res),
                             const.playerTileset, True, self))
        self.camera = Camera((0, 0, const.screenSize[0] * const.res, const.screenSize[1] * const.res),
                             (150, 200, 150, 200), self.get(0),
                             (self.map.size[0] * const.res, self.map.size[1] * const.res))
        self.background = Background(self.camera, const.backgrounds, self.map.getScale())
        self.editor = Editor(self.map, self.camera)
        self.sound = pygame.mixer.Sound("assets\\music.ogg")
        self.sound.play(-1)

    def addEntity(self, id=None, entity=None):
        if entity:
            if not id:
                self.entities[self.entityId] = entity
                entity.id = self.entityId
                self.entityId += 1
            else:
                self.entities[id] = entity

    def removeEntity(self, entity):
        del self.entities[entity.id]

    def get(self, entityId):
        return self.entities.get(entityId)

    def process(self, input):
        for entity in self.entities.values():
            if hasattr(entity, "controlled"):
                entity.tick(input)
            else:
                entity.tick([])
            if hasattr(entity, "weapon"):
                entity.weapon.tick()

    def render(self, surface):
        self.background.draw(surface, self.camera)
        for entity in self.entities.values():
            entity.display.draw(surface, self.camera)
            if hasattr(entity, "weapon"):
                entity.weapon.draw(surface, self.camera)
        self.map.draw(surface, self.camera)
        if self.editor.enabled:
            self.editor.draw(surface, self.camera)

    def getCloseEntity(self, name, location, range=100.):
        location = Vector2(*location)
        for entity in self.entities.values():
            if entity.name == name:
                distance = location.get_distance_to(entity.location)
            if distance < range:
                return entity
        return None

    def toggleEditor(self):
        global screen
        self.editor.enabled = not self.editor.enabled
        size = 2 if self.editor.enabled else 0
        screen = pygame.display.set_mode((screenSize[0] * res, screenSize[1] * res + size * res))

    def tick(self, inputs, surface):
        self.input(inputs)
        self.process(inputs)
        self.camera.tick()
        self.background.tick()

        if self.editor.enabled:
            self.editor.edit(inputs)

        self.render(surface)
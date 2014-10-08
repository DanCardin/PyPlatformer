import pygame
from map import *
from camera import *
from editor import *
from mchar import *
from const import *
from platform import *


class Level(object):
    def __init__(self, Levels):
        self.map = Map(Levels[0], Levels[1])
        self.map.initDrawMap()
        self.camera = None
        self.editor = None
        self.entities = {}
        self.entityId = 0
        self.background = pygame.surface.Surface((screenSize[0] * res, screenSize[1] * res))

    def start(self):
        self.entities = {}
        self.addEntity(MChar((self.map.start[0], self.map.start[1], 20, 26), (playerSpeed[0] * self.map.res, playerSpeed[1] * self.map.res), playerTileset, True, self))
        #for i in range(1):
        #    self.addEntity(Platform((96,416 - i * 32, 200, 10), (96,416 - i * 32, 20, 10), [randrange(1,4),randrange(1,4)], "assets\\platform.bmp", self))
        self.camera = Camera((0, 0, screenSize[0] * res, screenSize[1] * res), (150, 200, 150, 200), self.get(0), (self.map.size[0] * res, self.map.size[1] * res))
        self.editor = Editor(self.map, self.camera)

    def addEntity(self, entity):
        self.entities[self.entityId] = entity
        entity.id = self.entityId
        self.entityId += 1

    def removeEntity(self, entity):
        del self.entities[entity.id]

    def get(self, entityId):
        if entityId in self.entities:
            return self.entities[entityId]
        else:
            return None

    def process(self, input):
        for entity in self.entities.values():
            if hasattr(entity, "controlled"):
                entity.tick(input)
            else:
                entity.tick([])

    def render(self, surface):
        surface.blit(self.background, (0, 0))
        for entity in self.entities.values():
            entity.display.draw(surface, self.camera)
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

    def tick(self, input, surface):
        global screen
        self.process(input)
        self.camera.tick()
        if (pygame.KEYDOWN, pygame.K_e) in input:
            self.editor.enabled = not self.editor.enabled
            screen = pygame.display.set_mode((screenSize[0] * res, screenSize[1] * res + {False: 0, True: 2}[self.editor.enabled] * res))
        if self.editor.enabled:
            self.editor.edit(input)
        self.render(surface)

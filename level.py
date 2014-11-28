import const
from pygame import KEYDOWN, K_e, K_r
from pygame.mixer import Sound
from surface import Surface

from background import Background
from complete import Completion, Completeable
from camera import Camera
from countdown import CountdownTimer
from editor import Editor
from enemy import EnemyEmitter
from healthbar import HealthBar
from input import Input
from map import Map
from mchar import MChar
from object import Object
from wall import Tiles


class Level(Completeable):
    def __init__(self, surface, level):
        super().__init__()
        self._surface = surface
        self.map = Map(level[0], level[1])

    def start(self):
        self._scale = 2
        self.registered = {}
        self._entity_map = {}
        self._position_map = {}
        self._entities = {}

        self.map.load()
        for x, y in self.map.getMap().keys():
            self._position_map[(x, y)] = []
        self._total_surface = Surface((self.map.w, self.map.h))
        tid = self.addEntity(register=True,
                             entity=MChar(self.map.getStart(),
                                          (20, 26),
                                          const.playerSpeed,
                                          const.playerTileset, True, self, 5))
        self._camera = Camera(tuple([s * const.res for s in const.screenSize]),
                              self._total_surface,
                              self.map,
                              Object(150, 200, 150, 200),
                              self.get(tid))
        self._background = Background(self._camera,
                                      const.backgrounds)
        self.editor = Editor(self.map, self._surface)

        self.input = Input()
        self.input.set(KEYDOWN, K_e, "editor", self.editor.toggleEnabled)
        self.input.set(KEYDOWN, K_r, "restart", self.start)

        # self._sound = Sound("assets\\music.ogg")
        # self._sound.play(-1)

        self._healthBar = HealthBar(10, 10, self.get(tid))
        self._enemySpawn = EnemyEmitter(Object(50, 100, 0, 0), lambda: (0, 0), self, 2, 2)
        self._countdown = CountdownTimer(const.screenSize[0] * const.res - 50, 10, 100)

    def addEntity(self, register=False, entity=None):
        if not entity:
            raise Exception("Entity must not be None.")

        tid = entity.getId()
        reg = self.registered if register else self._entities

        reg[tid] = entity
        self._entity_map[tid] = set()
        return tid

    def removeEntity(self, entity):
        del self._entities[entity.id]

    def get(self, entityId):
        result = self._entities.get(entityId)
        if not result:
            result = self.registered.get(entityId)
        return result

    def process(self, inputs):
        for entity in self.registered.values():
            result = entity.tick(inputs)
            if Tiles.End in result.keys():
                self.setFinished()
            if not entity.isAlive():
                self.setLost()

        for entity in list(self._entities.values()):
            entity.tick()
            if not entity.isAlive():
                self._entities.pop(entity.getId())

        self._enemySpawn.tick()
        self._camera.tick()
        self._background.tick()
        self._countdown.tick()
        if self._countdown.isFinished():
            self.setLost()

        if self.editor.enabled():
            self.editor.tick(inputs, self._camera)

        if self.isComplete():
            pass
            # self._sound.fadeout(3000)

    def render(self):
        self._surface.fill((0, 0, 0))
        self._background.draw(self._total_surface, self._camera)
        self._enemySpawn.draw(self._total_surface, self._camera)
        for _entities in [self._entities, self.registered]:
            for entity in _entities.values():
                entity.draw(self._total_surface, self._camera)

        self.map.draw(self._total_surface, self._camera)
        self._healthBar.draw(self._total_surface)
        self._countdown.draw(self._total_surface)
        if self.editor.enabled():
            self.editor.draw(self._total_surface, self._camera)

        self._camera.draw(self._surface, self._scale)

        if self.editor.enabled():
            self.editor.menu.draw()

    def tick(self, inputs):
        self.input(inputs)
        self.process(inputs)
        self.render()

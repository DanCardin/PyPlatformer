import const
from pygame import KEYDOWN, K_e, K_r
from pygame.mixer import Sound
from surface import Surface

from parallax import Parallax
from complete import Completable
from viewport import Viewport
from countdown import CountdownTimer
from editor import Editor
from enemy import EnemySpawn
from healthbar import HealthBar
from input import Input, Inputable
from map import Map
from mchar import MChar
from object import Object
from wall import Tiles


class Level(Completable, Inputable):
    def __init__(self, surface, level, **kwargs):
        super().__init__(**kwargs)
        self._surface = surface
        self.map = Map(level[0], level[1])

    def start(self):
        self.map.load()
        self._entity_map = {}
        self._position_map = {}
        self._entities = {}
        self._registered = {}
        self._enemySpawns = {}
        for x, y in self.map.getMap().keys():
            self._position_map[(x, y)] = []

        self._total_surface = Surface((self.map.w, self.map.h))
        tid = self.addEntity(register=True,
                             entity=MChar(self,
                                          self.map.getType(Tiles.Start)[0],
                                          inputStream=self.getInputStream()))
        self._camera = Viewport(tuple([s * const.res for s in const.screenSize]),
                                lambda: self.map.getAttr("scale"),
                                self.get(tid),
                                (150, 200, 150, 200),
                                self.map)
        self._background = Parallax(const.backgrounds)
        self.editor = Editor(self.map,
                             self._surface,
                             enabled=False,
                             inputStream=self.getInputStream())

        self._input = Input(inputStream=self.getInputStream())
        self._input.set(KEYDOWN, self.editor.toggleEnabled, K_e)
        self._input.set(KEYDOWN, self.start, K_r)

        # self._sound = Sound("assets\\music.ogg")
        # self._sound.play(-1)

        try:
            self._healthBar = HealthBar(10, 10, self.get(tid))
        except AssertionError:
            pass

        for block in self.map.getType(Tiles.EnemySpawn):
            self._enemySpawns[block] = EnemySpawn(level=self,
                                                  anchor=Object(pos=(block.x, block.y)),
                                                  maxEmitted=block.getAttr("spawnNum"),
                                                  timeBetween=2)

        self._countdown = CountdownTimer(const.screenSize[0] * const.res - 50, 10,
                                         self.map.getAttr("timeLim"))

    def addEntity(self, register=False, entity=None):
        if not entity:
            raise Exception("Entity must not be None.")

        tid = entity.getId()

        self._entities[tid] = entity
        if register:
            self._registered[tid] = entity

        self._entity_map[tid] = set()
        return tid

    def removeEntity(self, entity):
        del self._entities[entity.id]

    def get(self, entityId):
        return self._entities.get(entityId)

    def process(self):
        for entity in self._entities.values():
            result = entity.tick()

            if not entity.isAlive():
                self._entities.pop(entity.getId())

            # This should generally only apply to playable characters.
            if entity in self._registered.values():
                if Tiles.End in result.keys():
                    self.setFinished()
                if not entity.isAlive():
                    self.setLost()

        for s in self._enemySpawns.values():
            s.tick()

        self._camera.tick()
        self._countdown.tick()
        if self._countdown.isFinished():
            self.setLost()

        if self.editor.enabled():
            self.editor.tick(self._camera)

        if self.isComplete():
            pass
            # self._sound.fadeout(3000)

    def render(self):
        self._surface.fill((0, 0, 0))
        self._background.draw(self._total_surface, self._camera)
        for s in self._enemySpawns.values():
            s.draw(self._total_surface)
        for entity in self._entities.values():
            entity.draw(self._total_surface)

        self.map.draw(self._total_surface)
        if self.editor.enabled():
            self.editor.draw(self._total_surface)

        self._camera.draw(self._surface, self._total_surface)

        self._healthBar.draw(self._surface)
        self._countdown.draw(self._surface)
        if self.editor.enabled():
            self.editor.menu.draw()

    def tick(self):
        self._input()
        self.process()
        self.render()

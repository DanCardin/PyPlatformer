import pygame
import const
from animation import Animation
from char import Health, Alive
from collision import Collision
from direction import Direction, Dir
from display import Display, Drawable
from files import Files
from gravity import GravityLine
from input import Input, Inputable
from jumping import Jumping
from events import Subscribee, MinTimeEventStream
from object import Object
from move import Move
from wall import Tiles
from weapons import Weapon
from ids import IDed


class Char(Object, Dir, IDed, Drawable, Health, Subscribee, Alive, Inputable):
    def __init__(self, level, speed, tileset, **kwargs):
        super().__init__(
            dirRule=lambda: {
                -1: Direction.Left,
                0: None,
                1: Direction.Right
            }[self.move.getDir(x=True)],
            **kwargs)
        self.collision = Collision(self, level)
        self.move = Move(self, speed, collision=self.collision)
        self._gravity = GravityLine(self, 2, h=level.map.h // 2)
        self.jumping = Jumping(self.move, self._gravity, 2)
        self._input = Input(inputStream=self.getInputStream())
        self.applyInputSettings()
        self._damageTimer = MinTimeEventStream(2)
        self._damageTimer.subscribe("self", self._takeDmg, autoInit=False)

        def _isMoving():
            return self.move.getSpeed(x=True) != 0

        def _hDir():
            return self.move.getDir(x=True)

        def _vDir():
            return {False: -1, True: 1}[self._gravity.positiveDir()]

        image = Files.loadImage(tileset)
        self._display = Display(image, self, Animation(image, 11, _isMoving, _hDir, _vDir), True)
        self._weapon = Weapon(level,
                              anchor=self,
                              offsetFunc=lambda: ((5 * self.getIntDir()), 0),
                              inputStream=self.getInputStream())

    def applyInputSettings(self):
        self._input.set(pygame.KEYDOWN, self.startMove, pygame.K_a, "left")
        self._input.set(pygame.KEYDOWN, self.startMove, pygame.K_d, "right")
        self._input.set(pygame.KEYDOWN, self.startMove, pygame.K_w, "up")
        self._input.set(pygame.KEYDOWN, self.startMove, pygame.K_s, "down")

        self._input.set(pygame.KEYUP, self.stopMove, pygame.K_a, "left")
        self._input.set(pygame.KEYUP, self.stopMove, pygame.K_d, "right")
        self._input.set(pygame.KEYUP, self.stopMove, pygame.K_w, "up")
        self._input.set(pygame.KEYUP, self.stopMove, pygame.K_s, "down")

    def startMove(self, arg):
        if arg == "left":
            self.move.setSpeed(x=-self.move.getTopSpeed(x=True))
        if arg == "right":
            self.move.setSpeed(x=self.move.getTopSpeed(x=True))
        if arg == "up":
            self.jumping.jump()

    def stopMove(self, arg):
        xspeed = self.move.getSpeed(x=True)
        if arg == "left" and xspeed < 0:
            self.move.setSpeed(x=0)
        if arg == "right" and xspeed > 0:
            self.move.setSpeed(x=0)
        if arg == "up":
            self.jumping.muteJump()

    def draw(self, surface, camera=Object()):
        self._display.draw(surface, camera)
        self._weapon.draw(surface, camera)

    def subscribe(self, id, callback, autoInit=True):
        self._damageTimer.subscribe(id, callback, autoInit)

    def unsubscribe(self, id):
        self._damageTimer.unsubscribe(id)

    def _takeDmg(self, ignore):
        self.decHealth(1)
        self.move.setSpeed(y=8)

    def tick(self):
        super().tick()
        self._input()
        self._weapon.tick()

        collisions = self.move()
        self.jumping.tick(collisions)
        self._gravity.tick(collisions)

        if collisions.get(Tiles.Deadly):
            self._damageTimer.notify()

        if self.getHealth() == 0:
            self.kill()

        return collisions


class MChar(Char):
    def __init__(self, level, start, **kwargs):
        super().__init__(level=level, pos=(start.x, start.y), size=const.playerSize,
                         speed=const.playerSpeed, tileset=const.playerTileset, baseHealth=5,
                         **kwargs)

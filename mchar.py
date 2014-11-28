import pygame
from animation import Animation
from char import Dir, Health, Alive
from collision import Collision
from display import Display, Drawable
from files import Files
from gravity import GravityLine
from input import Input
from jumping import Jumping
from libs.events import Subscribee, MinTimeEventStream
from object import Object
from move import Move
from wall import Tiles
from weapons import Weapon
from ids import Id


class MChar(Object, Dir, Id, Drawable, Health, Subscribee, Alive):
    def __init__(self, start, size, speed, tileset, control, level, maxHealth):
        Object.__init__(self, (start.x, start.y, size[0], size[1]))
        Dir.__init__(self, lambda: self.move.getDir(x=True))
        Id.__init__(self)
        Health.__init__(self, maxHealth)
        Alive.__init__(self)

        self.collision = Collision(self, level)
        self.move = Move(self, speed, collision=self.collision)
        self._gravity = GravityLine(self, 2, h=level.map.h // 2)
        self.jumping = Jumping(self.move, self._gravity, 2)
        self.input = Input()
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
        self._display = Display(image, self, True, Animation(image, 11, _isMoving, _hDir, _vDir))
        self._weapon = Weapon(self, lambda: ((5 * self.getDir()), 0), level)

    def applyInputSettings(self):
        self.input.set(pygame.KEYDOWN, pygame.K_a, "left", self.startMove, "left")
        self.input.set(pygame.KEYDOWN, pygame.K_d, "right", self.startMove, "right")
        self.input.set(pygame.KEYDOWN, pygame.K_w, "up", self.startMove, "up")
        self.input.set(pygame.KEYDOWN, pygame.K_s, "down", self.startMove, "down")

        self.input.set(pygame.KEYUP, pygame.K_a, "left", self.stopMove, "left")
        self.input.set(pygame.KEYUP, pygame.K_d, "right", self.stopMove, "right")
        self.input.set(pygame.KEYUP, pygame.K_w, "up", self.stopMove, "up")
        self.input.set(pygame.KEYUP, pygame.K_s, "down", self.stopMove, "down")

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

    def draw(self, surface, camera):
        self._display.draw(surface, camera)
        self._weapon.draw(surface, camera)

    def subscribe(self, id, callback):
        self._damageTimer.subscribe(id, callback)

    def unsubscribe(self, id):
        self._damageTimer.unsubscribe(id)

    def _takeDmg(self, ignore):
        self.decHealth(1)
        self.move.setSpeed(y=8)

    def tick(self, inputs):
        Dir.tick(self)
        self.input(inputs)
        self._weapon.tick(inputs)

        collisions = self.move()
        self.jumping.tick(collisions)
        self._gravity.tick(collisions)

        if collisions.get(Tiles.Deadly):
            self._damageTimer.notify()

        if self.getHealth() == 0:
            self.kill()

        return collisions

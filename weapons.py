from object import *
from move import *
from collision import *
from display import *
import itertools


class Bullet(Object):
    def __init__(self, Size, Speed, Tileset, Level, MaxRange):
        Object.__init__(self, Size)
        self.move = Move(Speed, self)
        self.collision = Collision(self, Level, "bullet")
        self.display = Display(Tileset, self, Size, False)
        self.dead = False
        self.move.speed[0] = self.move.topSpeed[0]
        self.move.speed[1] = self.move.topSpeed[1]
        self.dMoved = [0, 0]
        self.maxRange = MaxRange ** 2

    def tick(self):
        if not self.dead:
            if (self.dMoved[0] ** 2 + self.dMoved[1] ** 2) > self.maxRange:
                self.dead = True
            mRes = self.move.move()
            conditions = list(itertools.product(*[[1, 2, 3, "enemy", "bullet"], ["left", "right", "top", "bottom"]]))
            if [i for i in conditions if i in mRes]:
                self.dead = True
            self.dMoved[0] += self.move.speed[0]
            self.dMoved[1] += self.move.speed[1]


class Weapon(object):
    def __init__(self, Parent, Size, Speed, Tileset, Level, MaxRange):
        self.parent = Parent
        self.size = Size
        self.speed = Speed
        self.tileset = Tileset
        self.level = Level
        self.maxRange = MaxRange
        self.firedBullets = []

    def fire(self):
        speed = (self.speed * self.parent.dir[0], self.speed * self.parent.dir[1])

        temp = self.parent.rect
        if self.parent.dir[0] == 0:
            x = temp.x + temp.width / 2
        else:
            x = {True: temp.x + temp.width,
            False: temp.x - self.size[0]}[self.parent.dir[0] == 1]
        if self.parent.dir[1] == 0:
            y = temp.y + temp.height / 2
        else:
            y = {True: temp.y + temp.height,
            False: temp.y - self.size[1]}[self.parent.dir[1] == 1]

        self.firedBullets.append(Bullet((x, y, self.size[0], self.size[1]), speed, self.tileset, self.level, self.maxRange))

    def draw(self, surface, camera):
        for i in self.firedBullets:
            i.display.draw(surface, camera)

    def tick(self):
        for i in self.firedBullets:
            i.tick()
            if i.dead:
                self.firedBullets.remove(i)

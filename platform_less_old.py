from object import *
from collision import *
from display import *

class Platform(Object):
    def __init__(self, Rect, Size, Speed, Tileset, Level):
        Object.__init__(self, Size)
        self.collision = Collision(self, Level)
        self.display = Display(Tileset, self, Size, False)
        self.speed = Speed
        self.size = Rect

    def tick(self, inputs):
        if self.size[0] > self.x:
            self.speed[0] *= -1
            print "dd"
        if self.size[1] > self.y:
            self.speed[1] *= -1
            print "dy"
        if self.size[0] + self.size[2] <= self.x + self.w:
            self.speed[0] *= -1
            print "dd2"
        if self.size[1] + self.size[3] <= self.y + self.h:
            self.speed[1] *= -1
            print "dy2"

        self.x += self.speed[0]
        self.y += self.speed[1]

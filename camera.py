from object import Object
from object import *


class Camera(Object):
    def __init__(self, size, bounds, target, res):
        Object.__init__(self, size)
        self.target = target
        self.bounds = Rect(bounds)
        self.res = res

    def tick(self):
        if self.x > self.target.x - self.bounds.x:
            self.x = self.target.x - self.bounds.x
        if self.x < self.target.x + self.target.w + self.bounds.w - self.w:
            self.x = self.target.x + self.target.w + self.bounds.w - self.w

        if self.x < 0:
            self.x = 0
        if self.x + self.w > self.res[0]:
            self.x = (self.res[0]) - self.w
        if (self.x < 0) and (self.x + self.w > self.res[0]):
            self.x = self.target.x + self.target.w / 2 - self.w / 2

        if self.y > self.target.y - self.bounds.y:
            self.y = self.target.y - self.bounds.y
        if self.y < self.target.y + self.target.h + self.bounds.h - self.h:
            self.y = self.target.y + self.target.h + self.bounds.h - self.h

        if self.y < 0:
            self.y = 0
        if self.y + self.h > self.res[1]:
            self.y = (self.res[1]) - self.h
        if (self.y < 0) and (self.y + self.h > self.res[1]):
            self.y = self.target.y + self.target.h / 2 - self.h / 2

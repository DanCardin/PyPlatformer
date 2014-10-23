from object import Object


class Camera(Object):
    def __init__(self, size, bounds, target, res):
        Object.__init__(self, size)
        assert target is not None
        self.target = target
        self.bounds = Object(bounds)
        self.res = Object(res)

    def tick(self):
        if self.x > self.target.x - self.bounds.x:
            self.x = self.target.x - self.bounds.x
        if self.x < self.target.x + self.target.w + self.bounds.w - self.w:
            self.x = self.target.x + self.target.w + self.bounds.w - self.w

        if self.x < 0:
            self.x = 0
        if self.x + self.w > self.res.w:
            self.x = (self.res.w) - self.w
        if (self.x < 0) and (self.x + self.w > self.res.w):
            self.x = self.target.x + self.target.w / 2 - self.w / 2

        if self.y > self.target.y - self.bounds.y:
            self.y = self.target.y - self.bounds.y
        if self.y < self.target.y + self.target.h + self.bounds.h - self.h:
            self.y = self.target.y + self.target.h + self.bounds.h - self.h

        if self.y < 0:
            self.y = 0
        if self.y + self.h > self.res.h:
            self.y = (self.res.h) - self.h
        if (self.y < 0) and (self.y + self.h > self.res.h):
            self.y = self.target.y + self.target.h / 2 - self.h / 2

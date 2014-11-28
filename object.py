from pygame import Rect


class Objects(Rect):
    def __init__(self, *size):
        x, y, w, h = 0, 0, 0, 0
        le = len(size)
        if le == 0:
            pass
        elif le == 1:
            le0 = len(size[0])
            if le0 == 2:
                w, h = size[0]
            elif le0 == 4:
                x, y, w, h = size[0]
        elif le == 2:
            w, h = size
        elif le == 4:
            x, y, w, h = size
        else:
            raise ValueError("Object should take either 0, "
                             "1, 2, or 4 arguments, got %s." % str(size))

        super().__init__(x, y, w, h)


class Object(object):
    def __init__(self, *size):
        x, y, w, h = 0, 0, 0, 0
        le = len(size)
        if le == 0:
            pass
        elif le == 1:
            le0 = len(size[0])
            if le0 == 2:
                w, h = size[0]
            elif le0 == 4:
                x, y, w, h = size[0]
        elif le == 2:
            w, h = size
        elif le == 4:
            x, y, w, h = size
        else:
            raise ValueError("Object should take either 0, "
                             "1, 2, or 4 arguments, got %s." % str(size))

        self._rect = Rect(x, y, w, h)

    def asRect(self):
        return Rect(self.x, self.y, self.w, self.h)

    def copy(self):
        return self._rect.copy()

    def colliderect(self, collide):
        return self._rect.colliderect(collide.asRect())

    @property
    def top(self):
        return self._rect.top

    @top.setter
    def top(self, value):
        self._rect.top = value

    @property
    def bottom(self):
        return self._rect.bottom

    @bottom.setter
    def bottom(self, value):
        self._rect.bottom = value

    @property
    def left(self):
        return self._rect.left

    @left.setter
    def left(self, value):
        self._rect.left = value

    @property
    def right(self):
        return self._rect.right

    @right.setter
    def right(self, value):
        self._rect.right = value

    @property
    def x(self):
        return self._rect.x

    @x.setter
    def x(self, value):
        self._rect.x = value

    @property
    def y(self):
        return self._rect.y

    @y.setter
    def y(self, value):
        self._rect.y = value

    @property
    def w(self):
        return self._rect.w

    @w.setter
    def w(self, value):
        self._rect.w = value

    @property
    def h(self):
        return self._rect.h

    @h.setter
    def h(self, value):
        self._rect.h = value


class ObjectOffset(Object):
    def __init__(self, offset, *size):
        super(self).__init__(*size)

        self._offset = offset

    def changeOffset(self, offset):
        self._offset = offset

    @property
    def x(self):
        return self.x + self._offset.x

    @property
    def y(self):
        return self.y + self._offset.y

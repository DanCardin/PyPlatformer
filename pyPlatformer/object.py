from pygame import Rect
from scaleable import Scaled


class Object(object):
    def __init__(self, **kwargs):
        x, y, w, h = None, None, None, None
        if kwargs.get("rect", None):
            x, y, w, h = kwargs.pop("rect", None)
        elif kwargs.get("pos") or kwargs.get("size"):
            x, y = kwargs.pop("pos", (0, 0))
            w, h = kwargs.pop("size", (0, 0))
        else:
            x, y = kwargs.pop("x", 0), kwargs.pop("y", 0)
            w, h = kwargs.pop("w", 0), kwargs.pop("h", 0)

        super().__init__(**kwargs)

        assert None not in [x, y, w, h]

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

    def __repr__(self):
        return repr(self._rect)


class ScaledObject(Scaled):
    def __init__(self, **kwargs):
        self._scale = kwargs.pop("scale")
        self._object = Object(**kwargs)
        super().__init__(scale=self._scale)

    def unscaled(self):
        return self._object

    def copy(self):
        return self._object.copy()

    def asRect(self):
        return Rect(self.x, self.y, self.w, self.h)

    @property
    def x(self):
        return int(self._object.x + (self._object.w - self.w) / 2)

    @x.setter
    def x(self, value):
        self._object.x = value - (self._object.w - self.w) / 2

    @property
    def y(self):
        return int(self._object.y + (self._object.h - self.h) / 2)

    @y.setter
    def y(self, value):
        self._object.y = value - (self._object.h - self.h) / 2

    @property
    def w(self):
        return int(self._object.w * self.getScale())

    @property
    def h(self):
        return int(self._object.h * self.getScale())


class OffsetObject(Object):
    def __init__(self, **kwargs):
        self._offset = kwargs.pop("offset", Object())

        super().__init__(**kwargs)

    @property
    def x(self):
        return self._rect.x + self._offset.x

    @property
    def y(self):
        return self._rect.y + self._offset.y

    @property
    def w(self):
        return self._rect.w + self._offset.w

    @property
    def h(self):
        return self._rect.h + self._offset.h


class ScaledOffsetObject(OffsetObject, ScaledObject):
    pass

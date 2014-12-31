class Scaleable(object):
    def setScale(self, value):
        raise NotImplementedError()

    def getScale(self):
        raise NotImplementedError()


class Scaled(Scaleable):
    def __init__(self, **kwargs):
        self._scale = kwargs.pop("scale")
        self._eval = True if callable(self._scale) else False
        super().__init__(**kwargs)

    def setScale(self, value):
        self._scale = value
        self._eval = True if callable(self._scale) else False

    def getScale(self):
        if self._eval:
            return self._scale()
        return self._scale

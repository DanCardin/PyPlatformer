class Alive(object):
    def __init__(self, **kwargs):
        self._alive = kwargs.pop("alive", True)
        super().__init__(**kwargs)

    def kill(self):
        self._alive = False

    def isAlive(self):
        return self._alive

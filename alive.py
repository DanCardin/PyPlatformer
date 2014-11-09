class Alive(object):
    def __init__(self, default=True):
        self._alive = True

    def kill(self):
        self._alive = False

    def isAlive(self):
        return self._alive

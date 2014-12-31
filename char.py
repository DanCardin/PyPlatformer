class Dir(object):
    def __init__(self, **kwargs):
        self._rule = kwargs.pop("dirRule")
        self._dir = kwargs.pop("dirDefault", 1)
        super().__init__(**kwargs)

    def getDir(self):
        return self._dir

    def tick(self):
        curDir = self._rule()
        if curDir:
            self._dir = curDir


class Alive(object):
    def __init__(self, **kwargs):
        self._alive = kwargs.pop("alive", True)
        super().__init__(**kwargs)

    def kill(self):
        self._alive = False

    def isAlive(self):
        return self._alive


class Health(object):
    def __init__(self, **kwargs):
        self._baseHealth = kwargs.pop("baseHealth")
        self._health = self._baseHealth
        super().__init__(**kwargs)

    def setBaseHealth(self, value):
        self._baseHealth = value

    def getBaseHealth(self):
        return self._baseHealth

    def decHealth(self, value):
        self._health -= value

    def incHealth(self, value):
        self._health += value

    def resetHealth(self):
        self._health = self._baseHealth

    def getHealth(self):
        return self._health

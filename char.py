class Dir(object):
    def __init__(self, rule, default=1):
        self._rule = rule
        self._dir = 1

    def getDir(self):
        curDir = self._rule()
        if curDir:
            self._dir = curDir

        return self._dir


class Alive(object):
    def __init__(self, default=True):
        self._alive = True

    def kill(self):
        self._alive = False

    def isAlive(self):
        return self._alive


class Health(object):
    def __init__(self, baseHealth):
        self._baseHealth = baseHealth
        self._health = self._baseHealth

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

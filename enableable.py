class Enableable(object):
    def __init__(self, default=True):
        self._enabled = default

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def enabled(self):
        return self._enabled

    def toggleEnabled(self):
        self._enabled = not self._enabled

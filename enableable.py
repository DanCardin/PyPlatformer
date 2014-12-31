class Enableable(object):
    def __init__(self, **kwargs):
        self._enabled = kwargs.pop("enabled", True)
        super().__init__(**kwargs)

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def enabled(self):
        return self._enabled

    def toggleEnabled(self):
        self._enabled = not self._enabled

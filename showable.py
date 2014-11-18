class Showable(object):
    def __init__(self, default=True):
        self._showing = default

    def show(self):
        self._enabled = True

    def hide(self):
        self._enabled = False

    def showing(self):
        return self._enabled

    def toggleShowing(self):
        self._enabled = not self._enabled

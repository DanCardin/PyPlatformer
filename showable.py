class Showable(object):
    def __init__(self, **kwargs):
        self._showing = kwargs.pop("showing", True)
        super().__init__(**kwargs)

    def show(self):
        self._enabled = True

    def hide(self):
        self._enabled = False

    def showing(self):
        return self._enabled

    def toggleShowing(self):
        self._enabled = not self._enabled

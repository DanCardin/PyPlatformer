class Showable(object):
    """
    A partial class to enable something to be showable.

    Classes should inherit from this in order become `Showable`
    """
    def __init__(self, **kwargs):
        """
        `showing` - (Optional) The default state of the class.
        """
        self._showing = kwargs.pop("showing", True)
        super().__init__(**kwargs)

    def show(self):
        """
        Shows the `Showable`.
        """
        self._showing = True

    def hide(self):
        """
        Hides the `Showable`.
        """
        self._showing = False

    def showing(self):
        """
        Returns `True` if the `Showable` is showing.
        """
        return self._showing

    def toggleShowing(self):
        """
        Toggles the state of the `Showable` between showing and not showing.
        """
        self._showing = not self._showing

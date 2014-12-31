class Enableable(object):
    """
    Classes should inherit from this in order to become `Enableable`.
    """
    def __init__(self, **kwargs):
        """
        `enabled` - (Optional) The default state of the `Enableable`.
        """
        self._enabled = kwargs.pop("enabled", True)
        super().__init__(**kwargs)

    def enable(self):
        """
        Enables the `Enableable`.
        """
        self._enabled = True

    def disable(self):
        """
        Disables the `Enableable`.
        """
        self._enabled = False

    def enabled(self):
        """
        Returns `True` if the `Enableable` is enabled.
        """
        return self._enabled

    def toggleEnabled(self):
        """
        Toggles the `Enableable` between enabled and disabled.
        """
        self._enabled = not self._enabled

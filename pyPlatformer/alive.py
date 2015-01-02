class Alive(object):
    """
    Classes should inherit from this in order to be `Alive`. This means you can be either
    alive or killed.
    """
    def __init__(self, **kwargs):
        """
        Supplying an `alive` kwarg will set the initial aliveness. Defaults to `True`.
        """
        self._alive = kwargs.pop("alive", True)
        super().__init__(**kwargs)

    def kill(self):
        """
        Sets the aliveness to `False`.
        """
        self._alive = False

    def isAlive(self):
        """
        Returns `True` if alive or `False` if not.
        """
        return self._alive

    def reset(self):
        """
        Resets the aliveness to `True`.
        """
        self._alive = True

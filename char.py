class Alive(object):
    """
    A simple indicator of Aliveness.

    An instance can either be alive or dead, and thus can be killed.
    """
    def __init__(self, **kwargs):
        """
        `alive` - (Optional) The instance's initial `Alive` value. If not set, defaults to True.
        """
        self._alive = kwargs.pop("alive", True)
        super().__init__(**kwargs)

    def kill(self):
        """
        Sets the Aliveness of the instance to `False`.
        """
        self._alive = False

    def setAlive(self):
        """
        Sets the Aliveness of the instance to `True`.
        """
        self._alive = True

    def isAlive(self):
        """
        Returns `True` if the instance is alive and `False` if it is not.
        """
        return self._alive


class Health(object):
    """
    A Health-Point indicator
    """
    def __init__(self, **kwargs):
        """
        `baseHealth` - The health that the instance should be initialized to (and be reset to).
        """
        self._baseHealth = kwargs.pop("baseHealth")
        self._health = self._baseHealth
        super().__init__(**kwargs)

    def setBaseHealth(self, value):
        """
        Changes the `baseHealth` to `value`.
        """
        self._baseHealth = value

    def getBaseHealth(self):
        """
        Returns the `baseHealth`.
        """
        return self._baseHealth

    def decHealth(self, value):
        """
        Decreases the current `Health` value by `value`.
        """
        self._health -= value

    def incHealth(self, value):
        """
        Increases the current `Health` value by `value`.
        """
        self._health += value

    def resetHealth(self):
        """
        Resets the current `Health` value to `baseHealth`.
        """
        self._health = self._baseHealth

    def getHealth(self):
        """
        Returns the current `Health` value.
        """
        return self._health

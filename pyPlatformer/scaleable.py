class Scaleable(object):
    """
    Interface for things that can be scaled.
    """
    def setScale(self, value):
        """
        Subclasses need to override this method.
        """
        raise NotImplementedError()

    def getScale(self):
        """
        Subclasses need to override this method.
        """
        raise NotImplementedError()


class Scaled(Scaleable):
    """
    Classes should inherit from this in order to be scaleable.

    The scale can be either a value, or a callable. If it's a value, then
    the scale is just set. If it's a callable, it will be reevaluated from
    the return value of the callable every time `getScale` is called.
    """
    def __init__(self, **kwargs):
        """
        `scale` - The initial scale for the `Scaled` object.
        """
        self._scale = kwargs.pop("scale")
        self._eval = True if callable(self._scale) else False
        super().__init__(**kwargs)

    def setScale(self, scale):
        """
        `scale` - The new value for the scale of the `Scaleable`.
        """
        self._scale = scale
        self._eval = True if callable(self._scale) else False

    def getScale(self):
        """
        Returns the scale of the `Scaleable`
        """
        if self._eval:
            return self._scale()
        return self._scale

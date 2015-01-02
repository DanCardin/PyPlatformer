from enum import Enum


class Direction(Enum):
    Top = 1
    Bottom = 2
    Left = 3
    Right = 4


class Dir(object):
    """
    Classes should inherit from this in order to have a `Direction`.
    """
    def __init__(self, **kwargs):
        """
        `dirRule` - A `callable` that is evaluated to determine the direction that the instance
                    is facing. This `callable` should return a `Direction` or None.
        `dirDefault` - (Optional) The initial direction that the instance is facing. If not set,
                       defaults to `Direction.Right`.
        """
        self._rule = kwargs.pop("dirRule")
        self._dir = kwargs.pop("dirDefault", Direction.Right)
        super().__init__(**kwargs)

    def getDir(self):
        """
        Returns the current direction of the instance.
        """
        return self._dir

    def getIntDir(self):
        """
        Returns an integer representation of the `Direction`.
        """
        return {
            Direction.Left: -1,
            Direction.Right: 1,
        }[self._dir]

    def tick(self):
        """
        Reevaluates the direction using the `dirRule` to determine the current direction.
        """
        curDir = self._rule()
        if curDir:
            self._dir = curDir

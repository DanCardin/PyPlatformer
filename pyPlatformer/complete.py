from enum import Enum


class Completion(Enum):
    """
    An `Enum` to represent compleability states.
    """
    InProgress = 0
    Finished = 1
    Lost = 2


class Completable(object):
    """
    An indicator of Completability.
    """
    def __init__(self, **kwargs):
        """
        `progress` - (Optional) The default `progress` of the instance. Defaults to `InProgress`.
        """
        super().__init__(**kwargs)
        self._progress = kwargs.get("progress", Completion.InProgress)

    def isComplete(self):
        """
        Returns `True` if the completion status is either `Finished` or `Lost`.
        """
        return True if self._progress in [Completion.Finished, Completion.Lost] else False

    def isLost(self):
        """
        Returns `True` if the completion status is `Lost`.
        """
        return True if self._progress == Completion.Lost else False

    def isFinished(self):
        """
        Returns `True` if the completion status is `Finished`.
        """
        return True if self._progress == Completion.Finished else False

    def getProgress(self):
        """
        Returns the `Completion` variant that this instance is.
        """
        return self._progress

    def setProgress(self, value):
        """
        Sets the `Completion` status to `value`.
        """
        assert isinstance(value, Completion)
        self._progress = value

    def setInProgress(self):
        """
        Sets the `Completion` status to `InProgress`.
        """
        self._progress = Completion.InProgress

    def setFinished(self):
        """
        Sets the `Completion` status to `Finished`.
        """
        self._progress = Completion.Finished

    def setLost(self):
        """
        Sets the `Completion` status to `Lost`.
        """
        self._progress = Completion.Lost

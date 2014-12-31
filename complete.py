from enum import Enum


class Completion(Enum):
    InProgress = 0
    Finished = 1
    Lost = 2


class Completeable(object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._progress = kwargs.get("progress", Completion.InProgress)

    def isComplete(self):
        return True if self._progress in [Completion.Finished, Completion.Lost] else False

    def isLost(self):
        return True if self._progress == Completion.Lost else False

    def isFinished(self):
        return True if self._progress == Completion.Finished else False

    def getProgress(self):
        return self._progress

    def setProgress(self, value):
        assert isinstance(value, Completion)
        self._progress = value

    def setInProgress(self):
        self._progress = Completion.InProgress

    def setFinished(self):
        self._progress = Completion.Finished

    def setLost(self):
        self._progress = Completion.Lost

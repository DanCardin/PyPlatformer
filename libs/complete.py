class Completion(Enum):
    InProgress = 0
    Finished = 1
    Lost = 2

class Completeable(object):
	def __init__(self, default=Completion.InProgress):
        self._progress = default

    def isComplete

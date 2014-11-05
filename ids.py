class Id:
    __ids = 0

    def __init__(self):
        self._id = Id.__ids
        Id.__ids += 1

    def getId(self):
        return self._id

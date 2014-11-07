class Id:
    __ids = 0

    def __init__(self, altname=None):
        self._id = Id.__ids
        self._altname = altname
        Id.__ids += 1

    def getId(self):
        return self._id

    def getAltName(self):
        return self._altname

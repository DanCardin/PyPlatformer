class Id:
    __ids = 0

    def __init__(self, **kwargs):
        self._id = Id.__ids
        self._altname = kwargs.pop("idName", None)
        Id.__ids += 1
        super().__init__(**kwargs)

    def getId(self):
        return self._id

    def getAltName(self):
        return self._altname

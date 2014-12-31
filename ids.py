class IDed(object):
    """
    Classes should inherit from this in order to have an ID.
    """
    __ids = 0

    def __init__(self, **kwargs):
        """
        `idName` - (Optional) An identifier to associate with the `IDed`.
        """
        self._id = IDed.__ids
        self._altname = kwargs.pop("idName", None)
        IDed.__ids += 1
        super().__init__(**kwargs)

    def getId(self):
        """
        Returns the id of the `IDed`.
        """
        return self._id

    def getAltName(self):
        """
        Returns the alternate name associated with the `IDed`.
        """
        return self._altname

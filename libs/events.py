class EventStream(object):
    def __init__(self):
        self._observers = {}

    def _notify(self):
        for callback in self._observers.values():
            callback(self)

    def subscribe(self, id, callback):
        if not self._observers.get(id):
            self._observers[id] = callback
            callback(self)
        else:
            raise ValueError("id {} is already subscribed to {}".format(id, self))

    def unsubscribe(self, id):
        if not self._observers.pop(id):
            raise ValueError("id {} is not subscribed to {}".format(id, self))

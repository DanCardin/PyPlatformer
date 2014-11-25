import time


class EventStream(object):
    def __init__(self):
        self._observers = {}

    def notify(self):
        for callback in self._observers.values():
            callback(self)

    def subscribe(self, id, callback, autoInit=True):
        if not self._observers.get(id):
            self._observers[id] = callback
            if autoInit:
                callback(self)
        else:
            raise ValueError("id {} is already subscribed to {}".format(id, self))

    def unsubscribe(self, id):
        if not self._observers.pop(id):
            raise ValueError("id {} is not subscribed to {}".format(id, self))


class Subscribee(object):
    def subscribe(self, id, callback):
        raise NotImplementedError()

    def unsubscribe(self, id):
        raise NotImplementedError()


class MinTimeEventStream(EventStream):
    def __init__(self, duration):
        super().__init__()
        self._duration = duration
        self._lastTime = time.perf_counter()

    def notify(self):
        newTime = time.perf_counter()
        if newTime - self._lastTime > self._duration:
            self._lastTime = newTime
            super().notify()

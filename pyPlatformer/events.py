import time


class Subscribee(object):
    """
    An abstract base class for an object that is able to be subscribed to.
    """
    def subscribe(self, id, callback, autoInit=True):
        """
        Subscribes someone to object updates of this instance.

        `id` - Some unique identifier of the subscriber
        `callback` - The `callable` to call when updates occur.
        `autoInit` - (Optional) Automatically call the `callback` initially, before upates actually
                     occur.
        """
        raise NotImplementedError()

    def unsubscribe(self, id):
        """
        Unsubscribes `id` from receiving updates.
        """
        raise NotImplementedError()


class EventStream(Subscribee):
    """
    An implementation of `Subscribee` that notifies subscribers when updates occur.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._observers = {}

    def notify(self):
        """
        Calls the `callback` for each subscriber.
        """
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


class MinTimeEventStream(EventStream):
    """
    An `EventStream` that requires a minimum amount of time between notifications to subscribers.
    """
    def __init__(self, **kwargs):
        """
        `duration` - The duration of time that must pass between notifications.
        """
        self._duration = kwargs.pop("duration")
        super().__init__(**kwargs)

        self._lastTime = time.perf_counter()

    def notify(self):
        newTime = time.perf_counter()
        if newTime - self._lastTime > self._duration:
            self._lastTime = newTime
            super().notify()

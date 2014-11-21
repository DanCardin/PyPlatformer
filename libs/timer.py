import threading


class Timer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, interval, task)
        self._finished = threading.Event()
        self._interval = interval
        self._task = task

    def setInterval(self, interval):
        self._interval = interval

    def shutdown(self):
        self._finished.set()

    def run(self):
        while 1:
            if self._finished.isSet(): return
            self._task()
            self._finished.wait(self._interval)

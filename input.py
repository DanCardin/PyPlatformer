class Input(object):
    def __init__(self):
        self.keys = {}
        self.shortcuts = {}

    def set(self, event, key, label, action, arg=False):
        if not self.keys.get(key):
            self.keys[key] = label
        if not self.shortcuts.get(event):
            self.shortcuts[event] = {}
        self.shortcuts[event][label] = (action, arg)

    def use(self, event, key):
        action, argument = event[key]
        if action:
            if hasattr(action, "__call__"):
                if argument:
                    action(argument)
                else:
                    action()
            else:
                action = argument

    def __call__(self, inputs):
        if inputs is not None:
            for event, key in inputs:
                validEvent = self.shortcuts.get(event)
                validShortcut = self.keys.get(key)
                if validEvent and validShortcut:
                    if validEvent.get(validShortcut):
                        self.use(validEvent, validShortcut)

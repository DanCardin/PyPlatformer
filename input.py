class Input(object):
    """
    A class for managing inputs.

    After registering input events with `set(...)`, calls to this class will
    perform the specified actions on inputs that match the registered events.

    For example:
        set(KEYDOWN, exFunc, KEY_R, True)

        will call exFunc(True) when the R-keydown event is one of the events
        when this class is called.
    """
    def __init__(self):
        self._registeredEvents = {}

    def set(self, event, action, ident=None, arg=()):
        """
        Registers an event, with an action to perform upon seeing that event.

        `event` - The event to look for.
        `action` - The function to call on an event match.
        `ident` - (Optional) Information to further specify an `event`.
        `args` - (Optional) A tuple of arguments to pass to the `action`.
        """
        self._registeredEvents[(event, ident)] = (action, arg)

    def __call__(self, inputs):
        """
        Performs the registered actions upon matching the registered events.

        `inputs` - A list of inputs that can be used to match from.
        """
        for event in inputs:
            validEvent = self._registeredEvents.get((event.type, event.key))
            if validEvent:
                action, args = validEvent
                if isinstance(args, tuple):
                    action(*args)
                else:
                    action(args)

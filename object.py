from pygame import Rect


class Object(Rect):
    def __init__(self, size=(0, 0, 0, 0)):
        if len(size) == 2:
            Rect.__init__(self, 0, 0, size[0], size[1])
        else:
            Rect.__init__(self, size[0], size[1], size[2], size[3])

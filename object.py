from pygame import Rect


class Object(Rect):
    def __init__(self, Size=(0, 0, 0, 0)):
        if len(Size) == 2:
            Rect.__init__(self, 0, 0, Size[0], Size[1])
        else:
            Rect.__init__(self, Size[0], Size[1], Size[2], Size[3])

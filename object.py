from pygame import Rect


class Object(Rect):
    def __init__(self, *size):
        x, y, w, h = 0, 0, 0, 0
        le = len(size)
        if le == 0:
            pass
        elif le == 1:
            le0 = len(size[0])
            if le0 == 2:
                w, h = size[0]
            elif le0 == 4:
                x, y, w, h = size[0]
        elif le == 2:
            w, h = size
        elif le == 4:
            x, y, w, h = size
        else:
            raise ValueError("Object should take either 0, "
                             "1, 2, or 4 arguments, got %s." % str(size))

        super().__init__(x, y, w, h)

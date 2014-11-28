from pygame import surface
from pygame.rect import Rect


class Surface(surface.Surface):
    pass
    # def subsurface(self, rect):
    #     try:
    #         rect = Rect((rect.x, rect.y, rect.w, rect.h))
    #     except AttributeError:
    #         rect = Rect(rect)
    #     return super().subsurface(rect)

    # def blit(self, source, dest, area=None, special_flags=0):
    #     try:
    #         dest = Rect((dest.x, dest.y, dest.w, dest.h))
    #     except AttributeError:
    #         pass
    #     return super().blit(source, dest, area, special_flags)

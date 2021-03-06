import const
from math import ceil
from char import Health
from display import Display, Drawable
from files import Files
from object import Object
from surface import Surface


class HealthBar(Object, Drawable):
    def __init__(self, x, y, parent):
        super().__init__(pos=(x, y))
        assert isinstance(parent, Health)

        self._hearts = []
        self._parent = parent

        hearts = Files.loadImage(const.heartsImg)
        self._heartFilled = (hearts.subsurface(Object(rect=(0, 0, 10, 16)).asRect()),
                             hearts.subsurface(Object(rect=(10, 0, 10, 16)).asRect()))
        self._heartEmpty = (hearts.subsurface(Object(rect=(20, 0, 10, 16)).asRect()),
                            hearts.subsurface(Object(rect=(30, 0, 10, 16)).asRect()))

        self.update()

        self._parent.subscribe("healthbar", self.recalculate)

    def update(self):
        self._heartLen = self._parent.getBaseHealth()
        self.w, self.h = 10 * self._heartLen + 2 * ceil(self._heartLen / 2), 16

        surf = Surface((self.w, self.h))
        trans = self._heartFilled[0].get_at((0, 0))
        surf.fill(trans)
        surf.set_colorkey(trans)
        self._display = Display(surface=surf, klass=self)

        for i in range(self._heartLen):
            self._hearts.append(surf.subsurface(Object(rect=(10 * i + 2 * (i // 2), 0, 10, 16)).asRect()))

    def recalculate(self, parent):
        health = self._parent.getHealth()
        for i in range(self._heartLen):
            ind = i % 2
            heartType = self._heartFilled if (i + 1) <= health else self._heartEmpty
            self._hearts[i].blit(heartType[ind], (0, 0))

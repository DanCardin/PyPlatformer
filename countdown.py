import time
import const
from surface import Surface
from complete import Completeable
from display import Display, Drawable
from enableable import Enableable
from files import Files
from object import Object


class CountdownTimer(Object, Drawable, Enableable, Completeable):
    def __init__(self, x, y, maxTime, numNums=3):
        image, width = const.numbers
        numbers = Files.loadImage(image)
        numbers.set_colorkey(numbers.get_at((0, 0)))

        Object.__init__(self, x, y, width * numNums, numbers.get_height())
        Enableable.__init__(self, True)
        Completeable.__init__(self)

        self._numbers = []
        self._digits = []
        self._maxTime = maxTime
        self._currentTime = maxTime
        self._blank = Display(Surface((width, self.h)))

        for i in range(width):
            self._numbers.append(Display(numbers.subsurface((i * width, 0, width, self.h))))

        surf = Surface((self.w + 2 * numNums, self.h))
        self._display = Display(surf, self, transparent=True, alpha=200)
        for i in range(numNums):
            self._digits.append(surf.subsurface((i * width + 2 * i, 0, width, self.h)))

        self._lastUpdate = -maxTime

    def reset(self):
        self.setInProgress()
        self._currentTime = self.maxTime
        self.tick()

    def _getDigit(self, index):
        t = self._currentTime
        for i in range(len(self._digits) - index - 1):
            t = t // 10
        return t % 10

    def tick(self):
        if self._currentTime >= 0:
            newTime = time.perf_counter()
            if newTime - self._lastUpdate > 1:
                for i, digit in enumerate(self._digits):
                    self._blank.draw(digit)
                    self._numbers[self._getDigit(i)].draw(digit)
                self._currentTime -= 1
                self._lastUpdate = newTime
        else:
            self.setFinished()

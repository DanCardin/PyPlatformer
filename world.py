from level import Level


class World(object):
    def __init__(self, surface, levels):
        self.levels = []
        for i in levels:
            self.levels.append(Level(surface, i))
        self.currLevel = -1

    def nextLevel(self):
        if len(self.levels) > self.currLevel:
            self.currLevel += 1
            self._complete = False
        else:
            self._complete = True
        self.level = self.levels[self.currLevel]
        self.level.start()

    def prevLevel(self):
        if self.currLevel > 0:
            self.currLevel -= 1
        self.level.start()

    def isComplete(self):
        return self._complete

    def gameOver(self):
        ''

    def tick(self, input):
        self.level.tick(input)
        if self.level.isComplete():
            self.nextLevel()

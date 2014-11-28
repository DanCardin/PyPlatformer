from complete import Completeable
from level import Level


class World(Completeable):
    def __init__(self, surface, levels):
        super().__init__()
        self.levels = []
        for i in levels:
            self.levels.append(Level(surface, i))
        self.currLevel = -1

    def nextLevel(self):
        if self.currLevel < len(self.levels) - 1:
            self.currLevel += 1
            self.level = self.levels[self.currLevel]
            self.level.start()
        else:
            self.setProgress(self.level.getProgress())

    def prevLevel(self):
        if self.currLevel > 0:
            self.currLevel -= 1
        self.level.start()

    def tick(self, input):
        self.level.tick(input)
        if self.level.isComplete():
            if self.level.isLost():
                self.setLost()
            else:
                self.nextLevel()

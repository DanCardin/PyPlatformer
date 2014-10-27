from level import Level


class World(object):
    def __init__(self, surface, levels):
        self.levels = []
        for i in levels:
            self.levels.append(Level(surface, i))
        self.currLevel = 0
        self.level = self.levels[self.currLevel]

    def nextLevel(self):
        if len(self.levels) > self.currLevel:
            self.currLevel += 1

    def prevLevel(self):
        if self.currLevel > 0:
            self.currLevel -= 1

    def gameOver(self):
        ''

    def tick(self, input):
        self.level.tick(input)
        if self.level.isLevelComplete():
            self.nextLevel()

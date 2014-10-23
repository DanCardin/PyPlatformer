from level import Level


class World(object):
    def __init__(self, levels):
        self.levels = []
        for i in levels:
            self.levels.append(Level(i))
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

    def tick(self, input, surface):
        self.level.tick(input, surface)
        if self.level.isLevelComplete():
            self.nextLevel()

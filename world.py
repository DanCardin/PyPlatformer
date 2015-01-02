from complete import Completable
from input import Inputable
from level import Level


class World(Completable, Inputable):
    """
    A `Completable` collection of levels.
    """
    def __init__(self, surface, levels, **kwargs):
        """
        `surface` - The `Surface` that the `World` is drawn to.
        `levels` - A list of levels to create.
        `kwargs` - (Optional)
            `progress` - Default completion
            `inputStream` - The stream of input into the world.

            Any other `kwargs` will be passed through to each `Level`.
        """
        super().__init__(**kwargs)
        self.levels = []
        for level in levels:
            self.levels.append(Level(surface, level, **kwargs))
        self.currLevel = -1

    def nextLevel(self):
        """
        Goes to the next `Level`.

        Changes the status of the `World` to either `Finished` or `Lost`,
        if the current `Level` is the last `Level`.
        """
        if self.currLevel < len(self.levels) - 1:
            self.currLevel += 1
            self.level = self.levels[self.currLevel]
            self.level.start()
        else:
            self.setProgress(self.level.getProgress())

    def prevLevel(self):
        """
        Goes to the previous `Level`.
        """
        if self.currLevel > 0:
            self.currLevel -= 1
        self.level.start()

    def tick(self):
        """
        Manages the state of the `World`.

        Changes the `Completion` status of the `World`, and goes to the previous or next level
        when applicable.
        """
        self.level.tick()
        if self.level.isComplete():
            if self.level.isLost():
                self.setLost()
            else:
                self.nextLevel()

import pygame


class Files(object):
    def saveFile(self, input, file):
        fObj = open(file, "w")
        fObj.write(input)
        fObj.close()

    def _load_file(self, run):
        try:
            return run()
        except pygame.error as message:
            print("Cannot load file:", message)
            raise (message)

    def openFile(self, file):
        def run():
            fObj = open(file)
            s = fObj.read()
            fObj.close()
            return s
        return self._load_file(run)

    def loadImage(self, file, colorkey=None):
        def run():
            return pygame.image.load(file)

        image = self._load_file(run)
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

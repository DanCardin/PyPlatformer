import pygame
import os


class Files(object):
    @staticmethod
    def getFilePath(file):
        return os.path.join("assets", file)

    @staticmethod
    def saveFile(input, file):
        with open(Files.getFilePath(file), "w") as obj:
            obj.write(input)

    @staticmethod
    def _load_file(run):
        try:
            return run()
        except pygame.error as message:
            print("Cannot load file:", message)
            raise (message)

    @staticmethod
    def openFile(file):
        def run():
            with open(Files.getFilePath(file)) as obj:
                return obj.read()
        return Files._load_file(run)

    @staticmethod
    def loadImage(file, colorkey=None):
        def run():
            return pygame.image.load(Files.getFilePath(file))

        image = Files._load_file(run).convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

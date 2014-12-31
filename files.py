import os
import pygame


class Files(object):
    """
    A static class for loading files and assets and saving them.
    """

    __RelPath = "assets"

    @staticmethod
    def getFilePath(file):
        """
        Returns the path of the `file` asset.
        """
        return os.path.join(Files.__RelPath, file)

    @staticmethod
    def saveFile(file, input):
        """
        Writes `input` into `file`. This will overwrite everything in the file.
        """
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
        """
        Returns the contents of the `file`.
        """
        def run():
            with open(Files.getFilePath(file)) as obj:
                return obj.read()
        return Files._load_file(run)

    @staticmethod
    def loadImage(file, colorkey=None):
        """
        Loads and returns the image asset, `file`, with the optional colorkey to set.
        """
        def run():
            return pygame.image.load(Files.getFilePath(file))

        image = Files._load_file(run).convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

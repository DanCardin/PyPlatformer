import pygame
from object import Object
from files import Files
from display import Display


class Background(object):
    def __init__(self, camera, layers):
        self.camera = camera
        self._prevCameraPos = (self.camera.x, self.camera.y)
        self.layers = []
        for i, (size, damp, image) in enumerate(layers):
            self.layers.append(Layer(size, damp, image, i != 0))

    def draw(self, surface, camera):
        for i in self.layers:
            c = camera.copy()
            c.x -= camera.x - i.x
            c.y -= camera.y - i.y
            i.display.draw(surface, camera)

    def tick(self):
        diff = (self.camera.x - self._prevCameraPos[0],
                self.camera.y - self._prevCameraPos[1])
        if diff != (0, 0):
            for i in self.layers:
                if i.dampSpeed != 0:
                    i.x = (i.x + diff[0] / i.dampSpeed)
                    i.y = (i.y + diff[1] / i.dampSpeed)
        self._prevCameraPos = (self.camera.x, self.camera.y)


class Layer(Object):
    def __init__(self, size, dampSpeed, picture, transparency):
        Object.__init__(self, (0, 0, size[0], size[1]))
        self.dampSpeed = dampSpeed
        self.picture = Files.loadImage(picture)
        self.display = Display(self.picture, self, transparency)

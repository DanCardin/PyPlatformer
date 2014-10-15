import pygame
from object import Object
from files import Files
from display import Display


class Background(object):
    def __init__(self, camera, layers, scale):
        self.camera = camera
        self._prevCameraPos = (self.camera[0], self.camera[1])
        self.layers = []
        for i in layers:
            self.layers.append(Layer(i[0], i[1], i[2], scale))

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
        self._prevCameraPos = (self.camera[0], self.camera[1])


class Layer(Object):
    def __init__(self, size, dampSpeed, picture, scale):
        Object.__init__(self, (0, 0, size[0] * scale, size[1] * scale))
        self.dampSpeed = dampSpeed
        self.picture = pygame.transform.scale(Files().loadImage(picture),
                                              (self[2], self[3])).convert()
        self.display = Display(self.picture, self, self, True)
from object import Object
from files import Files
from display import Display, Drawable


class Parallax(Drawable):
    """
    Draws images that move at different speeds relative to eachother
    """
    def __init__(self, layers):
        """

        """
        self.layers = []
        for i, (size, damp, image) in enumerate(layers):
            self.layers.append([0, 0, Layer(size, damp, image, False if i == 0 else True)])

    def draw(self, surface, camera=Object()):
        try:
            _ = self._prevCameraPos
        except AttributeError:
            self._prevCameraPos = camera.asRect()

        for i, (x, y, layer) in enumerate(self.layers):
            if layer.getDampSpeed() != 0:
                # print(x, self.layers[i][0])
                self.layers[i][0] -= (camera.x - self._prevCameraPos.x) / layer.getDampSpeed()
                self.layers[i][1] -= (camera.y - self._prevCameraPos.y) / layer.getDampSpeed()
                layer.x = x
                layer.y = y
            layer.draw(surface)
        self._prevCameraPos = camera.asRect()


class Layer(Object, Drawable):
    def __init__(self, size, dampSpeed, picture, transparency):
        super().__init__(size=size)
        self._dampSpeed = dampSpeed
        self._picture = Files.loadImage(picture)
        self._display = Display(self._picture, self, transparency)

    def getDampSpeed(self):
        return self._dampSpeed

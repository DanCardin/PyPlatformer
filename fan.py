from object import *
from collision import *
from display import *

class Fan(Object):
    def __init__(self, Size, Tileset, Level):
        Object.__init__(self, Size)
        self.collision = Collision(self, Level)
        self.display = Display(Tileset, self, Size, False)
        
    def tick(self, inputs):
        
from object import *
from collision import *
from display import *

class Platform(Object):
    def __init__(self, Size, Paths, Tileset):
        Object.__init__(self, Size)
        #self.collision = Collision(self, Level)
        self.display = Display(Tileset, self, Size, False)
        self.paths = Paths
        
    def tick(self):
        ''''''
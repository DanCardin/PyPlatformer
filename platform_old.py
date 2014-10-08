from object import *
from move import *
from collision import *
from display import *

class Platform(Object):
    def __init__(self, Size, Speed, Tileset, Control, Level):
        Object.__init__(self, Size)
        #self.input = Input()
        self.move = Move(Speed, self)
        self.collision = Collision(self, Level)
        self.display = Display(Tileset, self, Size, False)
        self.move.speed[0] = self.move.topSpeed[0]
        self.move.speed[1] = self.move.topSpeed[1]
        self.controlled = Control
        self.inertia = 2
        
    def tick(self, inputs):
        check = self.move.move()
        if check[1] != 0:
            if check[1] in (1,2):
                self.move.speed[0] = -self.move.speed[0]
            if check[1] in (3,4):
                self.move.speed[1] = -self.move.speed[1]
class Molecule:
    def __init__(self,index, pos_x, pos_y):
        self.index = index
        self.pos_x = pos_x
        self.pos_y = pos_y

class Movement_chance:
    def __init__(self, direction,probability):
        self.dir = direction
        self.prob = probability

class Direction_movement:
    def __init__(self, index, direction, probability):
        self.index = index
        self.dir = direction
        self.prob = probability
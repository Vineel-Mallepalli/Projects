
def match(piece):
    pass


class Piece:
    # this will be the super class for all chess pieces.
    # x_pos and y_pos will be index-1 (range from 1 to 8)
    # This corresponds with chess notation and board numbering.
    def __init__(self, x_pos, y_pos, color):
        self.x = x_pos
        self.y = y_pos
        self.color = color

    def draw(self):
        pass



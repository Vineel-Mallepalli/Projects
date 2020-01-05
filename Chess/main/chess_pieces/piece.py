def validate(x, y, color):
    if 1 <= x <= 8 and 1 <= y <= 8 and (color == "white" or color == "black"):
        return x, y, color
    return ValueError("incorrect input values for Piece")


class Piece:
    # this will be the super class for all chess pieces.
    # x_pos and y_pos will be index-1 (range from 1 to 8)
    # This corresponds with chess notation and board numbering.
    def __init__(self, x_pos, y_pos, color):
        self.x, self.y, self.color = validate(x_pos, y_pos, color)

    # Later: figure out GUI
    def draw(self):
        pass



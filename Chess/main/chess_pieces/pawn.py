from Chess.main.chess_pieces.piece import Piece


def validate(x, y, color):
    if 1 <= x <= 8 and 2 <= y <= 7 and (color == "white" or color == "black"):
        return x, y, color
    return ValueError("incorrect input values for Pawn")


class Pawn(Piece):
    def __init__(self, x_pos, y_pos, color):
        super(Pawn, self).__init__(x_pos, y_pos, color)
        self.x, self.y, self.color = validate(x_pos, y_pos, color)
        self.value = 1

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

    # Will transfer full functionality to board later.
    def get_valid_moves(self):
        valid_moves = []
        if 1 < self.y <= 7:
            valid_moves.append((self.x, self.y + 1))
            if self.y == 2:
                valid_moves.append((self.x, self.y + 2))
            if 1 <= self.x - 1 <= 8:
                valid_moves.append((self.x - 1, self.y + 1))
            if 1 <= self.x + 1 <= 8:
                valid_moves.append((self.x + 1, self.y + 1))
        return valid_moves

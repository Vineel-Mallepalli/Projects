from Chess.main.chess_pieces.piece import Piece


class Rook(Piece):
    def __init__(self, x_pos, y_pos, color):
        super(Rook, self).__init__(x_pos, y_pos, color)
        self.value = 5

    # Will transfer full functionality to board later.
    def get_valid_moves(self):
        valid_moves = []
        for x_inc in range(7):
            valid_moves.append((((self.x + x_inc) % 8) + 1, self.y))
        for y_inc in range(7):
            valid_moves.append((self.x, ((self.y + y_inc) % 8) + 1))
        return valid_moves

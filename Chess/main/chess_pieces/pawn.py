from Chess.main.chess_pieces.piece import Piece


class Pawn(Piece):
    # constructor same as super class, is there a way to simplify?
    def __init__(self, x_pos, y_pos, color):
        super(Pawn, self).__init__(x_pos, y_pos, color)
        self.value = 1

    # inherits draw method automatically from Piece.
    # this method limits squares, then board will check among these.
    # Might transfer full functionality to board later.
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

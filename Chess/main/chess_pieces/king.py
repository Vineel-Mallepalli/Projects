from Chess.main.chess_pieces.piece import Piece


class King(Piece):
    # constructor same as super class, is there a way to simplify?
    def __init__(self, x_pos, y_pos, color):
        super(King, self).__init__(x_pos, y_pos, color)
        self.value = 0

    # inherits draw method automatically from Piece.
    # this method limits squares, then board will check among these.
    # Might transfer full functionality to board later.
    def get_valid_moves(self):
        # king can move one move in any direction, but cannot stay in the same square.
        valid_moves = []
        idx_changes = [-1, 0, 1]
        valid_moves.extend([[(self.x + x_change, self.y + y_change) for x_change in idx_changes
                             if 1 <= self.x + x_change <= 8 and 1 <= self.y + y_change <= 8 and
                             (x_change != 0 or y_change != 0)] for y_change in idx_changes])
        return valid_moves

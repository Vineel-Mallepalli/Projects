from Chess.main.chess_pieces.piece import Piece


class Bishop(Piece):
    # constructor same as super class, is there a way to simplify?
    def __init__(self, x_pos, y_pos, color):
        super(Bishop, self).__init__(x_pos, y_pos, color)
        self.x = x_pos
        self.y = y_pos
        self.color = color
        self.value = 3

    # inherits draw method automatically from Piece.
    # this method limits squares, then board will check among these.
    # Might transfer full functionality to board later.
    def get_valid_moves(self):
        valid_moves = []
        first_quadrant_moves = [(self.x + xy_inc + 1, self.y + xy_inc + 1) for xy_inc in range(7)
                                if 1 <= self.x + xy_inc + 1 <= 8 and 1 <= self.y + xy_inc + 1 <= 8]
        second_quadrant_moves = [(self.x - xy_inc - 1, self.y + xy_inc + 1) for xy_inc in range(7)
                                 if 1 <= self.x - xy_inc - 1 <= 8 and 1 <= self.y + xy_inc + 1 <= 8]
        third_quadrant_moves = [(self.x - xy_inc - 1, self.y - xy_inc - 1) for xy_inc in range(7)
                                if 1 <= self.x - xy_inc - 1 <= 8 and 1 <= self.y - xy_inc - 1 <= 8]
        fourth_quadrant_moves = [(self.x + xy_inc + 1, self.y - xy_inc - 1) for xy_inc in range(7)
                                 if 1 <= self.x + xy_inc + 1 <= 8 and 1 <= self.y - xy_inc - 1 <= 8]
        valid_moves.extend(first_quadrant_moves)
        valid_moves.extend(second_quadrant_moves)
        valid_moves.extend(third_quadrant_moves)
        valid_moves.extend(fourth_quadrant_moves)
        return valid_moves

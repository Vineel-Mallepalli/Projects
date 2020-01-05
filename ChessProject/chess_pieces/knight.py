from ChessProject.chess_pieces.piece import Piece


class Knight(Piece):
    # constructor same as super class, is there a way to simplify?
    def __init__(self, x_pos, y_pos, color):
        super(Knight, self).__init__(x_pos, y_pos, color)
        self.x = x_pos
        self.y = y_pos
        self.color = color
        self.value = 3

    # inherits draw method automatically from Piece.
    # this method limits squares, then board will check among these.
    # Might transfer full functionality to board later.
    def get_valid_moves(self):
        unbounded_moves = []
        unbounded_moves.extend([(self.x - 2, self.y - 1), (self.x - 2, self.y + 1),
                                (self.x - 1, self.y - 2), (self.x - 1, self.y + 2),
                                (self.x + 1, self.y - 2), (self.x + 1, self.y + 2),
                                (self.x + 2, self.y - 1), (self.x + 2, self.y + 1)])
        valid_moves = list(filter(lambda tup: 1 <= tup[0] <= 8 and 1 <= tup[1] <= 8, unbounded_moves))
        return valid_moves

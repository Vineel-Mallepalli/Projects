from Chess.main.chess_pieces.piece import Piece


class King(Piece):
    def __init__(self, x_pos, y_pos, color):
        super(King, self).__init__(x_pos, y_pos, color)
        self.value = 0


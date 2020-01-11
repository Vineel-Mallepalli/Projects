from Chess.main.chess_pieces.piece import Piece


class Rook(Piece):
    def __init__(self, x_pos, y_pos, color):
        super(Rook, self).__init__(x_pos, y_pos, color)
        self.value = 5

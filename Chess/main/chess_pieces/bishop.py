from Chess.main.chess_pieces.piece import Piece


class Bishop(Piece):
    def __init__(self, x_pos, y_pos, color):
        super(Bishop, self).__init__(x_pos, y_pos, color)
        self.value = 3

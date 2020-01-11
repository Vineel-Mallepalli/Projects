from Chess.main.chess_pieces.piece import Piece


class Queen(Piece):
    # constructor same as super class, is there a way to simplify?
    def __init__(self, x_pos, y_pos, color):
        super(Queen, self).__init__(x_pos, y_pos, color)
        self.value = 9
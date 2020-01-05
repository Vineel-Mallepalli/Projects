from ChessProject.chess_pieces import bishop, king, knight, pawn, queen, rook
from ChessProject import constants
from ChessProject.chess_board.board import Board


class StartBoard(Board):

    def __init__(self):
        super(StartBoard, self).__init__()
        self.board = constants.START_BOARD
        self.counts = constants.START_COUNTS
        self.score = 0

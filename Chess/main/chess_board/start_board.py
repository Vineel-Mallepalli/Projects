from Chess.main.chess_board.board import Board
from Chess import constants


class StartBoard(Board):

    def __init__(self):
        super(StartBoard, self).__init__()
        self.board = constants.START_BOARD
        self.counts = constants.START_COUNTS
        self.score = 0

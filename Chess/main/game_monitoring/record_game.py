from Chess.main.chess_board import start_board


class Game:
    # record each board in a dict for quick, easy lookup.
    # dict is formatted {move_number: Board}
    def __init__(self):
        self.boards = {0: start_board.StartBoard()}
        self.current = 0

    def add_board(self, move_num, board):
        self.current = move_num
        self.boards[move_num] = board

    def draw_board(self):
        # draw(self.boards[self.current])
        pass

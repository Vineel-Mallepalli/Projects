from Chess.main.chess_pieces import knight, bishop, queen, king, pawn, rook
from Chess import constants
from collections import Counter


# need some way to track game state. normal, check, checkmate.

# redo this method. Use Counter to count type of piece (separate by color) and store
# a dict of how many pieces of each color exist with the board. Then use that to calc score.
# tldr; reconfigure to use get_counts() to calc_score.
def calc_score(counts):
    if counts == constants.START_COUNTS:
        return 0
    score = 0
    multiplier = 1
    for color, piece in counts.keys():
        if color == "black":
            multiplier = -1
        if piece == "pawn":
            score += (multiplier * 1)
        elif piece == "rook":
            score += (multiplier * 5)
        elif piece == "knight" or piece == "bishop":
            score += (multiplier * 3)
        elif piece == "queen":
            score += (multiplier * 9)
        else:
            continue
    return score


#  use Counter to count type of piece for each color and store in a dict per color.
def get_counts(arr):
    if not validate_board(arr):
        return AssertionError
    if arr == constants.START_BOARD:
        return constants.START_COUNTS
    counter = Counter()
    for row in range(len(arr)):
        for col in range(len(arr)):
            obj = arr[row][col]
            if isinstance(obj, rook.Piece):
                counter[type_to_str(obj)] += 1
    return counter


# LATER: try and combine get_counts and get_pieces
def get_pieces(arr):
    if arr == constants.START_BOARD:
        return constants.START_PIECES
    white_pieces = set()
    black_pieces = set()
    for row in range(len(arr)):
        for col in range(len(arr)):
            obj = arr[row][col]
            if isinstance(obj, rook.Piece):
                if obj.color == "white":
                    white_pieces.add(obj)
                else:
                    black_pieces.add(obj)
    return white_pieces, black_pieces


def type_to_str(piece):
    color = "black"
    if not isinstance(piece, rook.Piece):
        return TypeError
    if piece.color == "white":
        color = "white"
    if isinstance(piece, pawn.Pawn):
        return color, "pawn"
    elif isinstance(piece, rook.Rook):
        return color, "rook"
    elif isinstance(piece, knight.Knight):
        return color, "knight"
    elif isinstance(piece, bishop.Bishop):
        return color, "bishop"
    elif isinstance(piece, queen.Queen):
        return color, "queen"
    elif isinstance(piece, king.King):
        return color, "king"
    else:
        return TypeError


# make 2 is_valid: second one checks counts.
def validate_board(arr):
    # make sure: the board is 8x8
    # every square is either a Piece, or ""
    # no two pieces are at the same location
    # no pawn is on the first rank or 8th rank
    if len(arr) != 8:  # check arr has 8 rows
        return False
    for row in arr:  # check arr has 8 cols
        if len(row) != 8:
            return False
    squares = [[False for _ in range(8)] for __ in range(8)]
    for row in arr:
        for col in arr:
            if isinstance(arr[row][col], rook.Piece):
                if squares[row][col]:
                    return False
                squares[row][col] = True
                # pawn can't be in row 1 or row 8
                if isinstance(arr[row][col], pawn.Pawn) and (row < 1 or row >= 7 or col < 1 or col > 8):
                    return False
            else:
                if arr[row][col] != "":
                    return False
    return True


def validate_counts(counts):
    # for each color: max 1 king, max 8 pawns
    if counts["white"]["king"] > 1 or counts["black"]["king"] > 1:
        if counts["white"]["pawn"] > 8 or counts["black"]["pawn"] > 8:
            return False
    return True


def clear():
    return Board([["" for _ in range(8)] for __ in range(8)])


def reset():
    return Board(constants.START_BOARD)
    # board [fir][sec]: fir = 8 - y; sec = x - 1


def move(board, piece, square):
    # INPUTS: board, piece (BUT turn-based), square to move the piece to
    # OUTPUT: new board instance with the resulting movement.
    # first, check piece chosen is the color whose turn it is.
    # MAYBE: check occupied squares and piece is right color before move() is called to reduce num calls.
    # MAYBE: check BEFORE you call this function for efficiency. Also prevents need to create, manage, and return
    # instances of the same exact board.
    # make sure square is not occupied.
    # if square is occupied, check color.
    # make sure the piece can move to that square.
    # make sure there are no pieces in the way.
    # specific rules for king, pawn, check if after move, opposing king is in check.
    # PAWN:
    # can only move diagonal if opposing piece present.
    # can only move forward if NO opposing piece present.
    # en passant: check pawn on 5th rank if white, 4th rank if black. check
    # most recent move to see if it was 2-square pawn move in adjacent file
    # KING:
    # BUT WHAT ABOUT DISCOVERED CHECKS? CHECK ALL THE PIECES each move.
    # BUT WHAT ABOUT PINS? IF MOVING PIECE RESULTS IN OWN KING ATTACKED, don't allow.
    # IF OPPOSING KING IN CHECK: alter game state, check king possible squares.
    # maybe: for each board instance, keep track of each piece's attacked squares
    # king CANNOT move into any of these attacked squares.
    color_to_move = board.to_move
    if board.state == "normal":
        if piece.color == color_to_move:
            pieces = board.white_pieces.union(board.black_pieces)
            for piece in pieces:
                if square.x == piece.x and square.y == piece.y:  # square is occupied, LATER: code captures.
                    return board
                if (square.x, square.y) not in piece.get_valid_moves:
                    return board
                if isinstance(piece, queen.Queen) or isinstance(piece, bishop.Bishop) or isinstance(piece, pawn.Pawn) or isinstance(piece, rook.Rook):
                    is_obstructed(piece, pieces, square)
                    # check for Check. see if opposing color pieces are attacking current color king after move.
                    is_pinned(board, pieces)

    pass


def is_obstructed(piece, pieces, square):
    pass


def is_pinned(board, piece, squares, pieces):
    # if is pinned, can still move along direction of check
    pass


class Board:
    # later: add move number and store each board externally so can move back and forth.
    # represent board as [][].
    # this will be implemented using functional programming.
    # store white pieces and black pieces in set. Now, we don't have to iterate through
    # ALL 64 squares for functions, we can choose to only iterate through the squares with pieces.
    # don't calculate all possible moves, just check if queried move is acceptable.
    # 3 states: normal, in check, checkmate (how to know which color is in check/checkmate?)
    # Assumption: if it is check and black's turn, black is in check.
    # (or else the previous move is disallowed)
    # Assumption: if it is checkmate and black's turn, black is in checkmate and has lost.
    def __init__(self, arr=constants.START_BOARD, to_move="white", state="normal"):
        self.board = arr
        self.counts = get_counts(arr)
        self.score = calc_score(self.counts)
        self.to_move = to_move
        self.state = state
        self.white_pieces, self.black_pieces = get_pieces(arr)

    def move(self):
        pass

    def get_score(self):
        return self.score

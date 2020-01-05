from Chess.main.chess_pieces import knight, bishop, queen, king, pawn, rook
from Chess import constants
from collections import Counter


# need some way to track game state. normal, check, checkmate.

# use dict of how many pieces of each color exist with the board to calc score.
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


# Use to categorize every piece by color and type
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


# make 2 is_valid: second one checks counts
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


# make sure num of each type does not exceed maximum possible
def validate_counts(counts):
    # for each color: max 1 king, max 8 pawns
    if counts["white"]["king"] > 1 or counts["black"]["king"] > 1:
        if counts["white"]["pawn"] > 8 or counts["black"]["pawn"] > 8:
            return False
    return True


# empty the board
def clear():
    return Board([["" for _ in range(8)] for __ in range(8)])


# return the starting board, equivalent to starting a new game
def reset():
    return Board(constants.START_BOARD)
    # board [fir][sec]: fir = 8 - y; sec = x - 1


# if legal, move the piece selected to the square and return resulting board
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
                if isinstance(piece, queen.Queen) or isinstance(piece, bishop.Bishop) \
                        or isinstance(piece, pawn.Pawn) or isinstance(piece, rook.Rook):
                    # check for Check. see if opposing color pieces are attacking current color king after move.
                    is_pinned(board, pieces)
                    # UNFINISHED. WORK ON after keeping track of obstructing pieces and attacked squares.
    pass


# check if a piece is pinned
def is_pinned(new_board, piece, square, pieces):
    # if is pinned, can move along direction of check. easiest way. If move is possible, check for Check in new board.
    # before calling, move piece to requested square. pass new board in as parameter
    # Assumption: we have already checked that the piece can physically move to the square.
    # Now, we check if own king is in attacked squares.
    pass


# get list of squares attacked by a rook, taking into account other pieces on the board
def get_rook_attacked_squares(board, piece):
    if not isinstance(piece, rook.Rook) and not isinstance(piece, queen.Queen):
        return TypeError
    attacked_squares = []
    color = "white" if piece.color == "white" else "black"
    other_color = "white" if color == "black" else "black"

    # check squares to the right
    x_inc = 1
    while piece.x + x_inc <= 8:
        if (piece.x + x_inc, piece.y) in board.locations.get(color):
            break
        elif (piece.x + x_inc, piece.y) in board.locations.get(other_color):
            attacked_squares.append((piece.x + x_inc, piece.y))
            break
        else:
            attacked_squares.append((piece.x + x_inc, piece.y))
            x_inc += 1

    # check squares to the left
    x_dec = 1
    while piece.x - x_dec >= 1:
        if (piece.x - x_dec, piece.y) in board.locations.get(color):
            break
        elif (piece.x - x_dec, piece.y) in board.locations.get(other_color):
            attacked_squares.append((piece.x - x_dec, piece.y))
            break
        else:
            attacked_squares.append((piece.x - x_dec, piece.y))
            x_dec += 1

    # check squares above
    y_inc = 1
    while piece.y + y_inc <= 8:
        if (piece.x, piece.y + y_inc) in board.locations.get(color):
            break
        elif (piece.x, piece.y + y_inc) in board.locations.get(other_color):
            attacked_squares.append((piece.x, piece.y + y_inc))
            break
        else:
            attacked_squares.append((piece.x, piece.y + y_inc))
            y_inc += 1

    # check squares below
    y_dec = 1
    while piece.y - y_dec >= 1:
        if (piece.x, piece.y - y_dec) in board.locations.get(color):
            break
        elif (piece.x, piece.y - y_dec) in board.locations.get(other_color):
            attacked_squares.append((piece.x, piece.y - y_dec))
            break
        else:
            attacked_squares.append((piece.x, piece.y - y_dec))
            y_dec += 1

    return attacked_squares


# get list of squares attacked by a bishop, taking into account other pieces on the board
def get_bishop_attacked_squares(board, piece):
    if not isinstance(piece, bishop.Bishop) and not isinstance(piece, queen.Queen):
        return TypeError
    attacked_squares = []
    color = "white" if piece.color == "white" else "black"
    other_color = "white" if color == "black" else "black"

    # find first quadrant moves
    xy_inc = 1
    while piece.x + xy_inc <= 8 and piece.y + xy_inc <= 8:
        if (piece.x + xy_inc, piece.y + xy_inc) in board.locations.get(color):
            break
        elif (piece.x + xy_inc, piece.y + xy_inc) in board.locations.get(other_color):
            attacked_squares.append((piece.x + xy_inc, piece.y + xy_inc))
            break
        else:
            attacked_squares.append((piece.x + xy_inc, piece.y + xy_inc))
            xy_inc += 1

    # find second quadrant moves
    x_dec_y_inc = 1
    while piece.x - x_dec_y_inc >= 1 and piece.y + x_dec_y_inc <= 8:
        if (piece.x - x_dec_y_inc, piece.y + x_dec_y_inc) in board.locations.get(color):
            break
        elif (piece.x - x_dec_y_inc, piece.y + x_dec_y_inc) in board.locations.get(other_color):
            attacked_squares.append((piece.x - x_dec_y_inc, piece.y + x_dec_y_inc))
            break
        else:
            attacked_squares.append((piece.x - x_dec_y_inc, piece.y + x_dec_y_inc))
            x_dec_y_inc += 1

    # find third quadrant moves
    x_inc_y_dec = 1
    while piece.x + x_inc_y_dec <= 8 and piece.y - x_inc_y_dec >= 1:
        if (piece.x + x_inc_y_dec, piece.y - x_inc_y_dec) in board.locations.get(color):
            break
        elif (piece.x + x_inc_y_dec, piece.y - x_inc_y_dec) in board.locations.get(other_color):
            attacked_squares.append((piece.x + x_inc_y_dec, piece.y - x_inc_y_dec))
            break
        else:
            attacked_squares.append((piece.x + x_inc_y_dec, piece.y - x_inc_y_dec))
            x_inc_y_dec += 1

    # find fourth quadrant moves
    xy_dec = 1
    while piece.x - xy_dec >= 1 and piece.y - xy_dec >= 1:
        if (piece.x - xy_dec, piece.y - xy_dec) in board.locations.get(color):
            break
        elif (piece.x - xy_dec, piece.y - xy_dec) in board.locations.get(other_color):
            attacked_squares.append((piece.x - xy_dec, piece.y - xy_dec))
            break
        else:
            attacked_squares.append((piece.x - xy_dec, piece.y - xy_dec))
            xy_dec += 1

    return attacked_squares


# get list of squares attacked by a king, taking into account other pieces on the board
def get_king_attacked_squares(board, piece):
    if not isinstance(piece, king.King):
        return TypeError
    color = "white" if piece.color == "white" else "black"
    idx_changes = [-1, 0, 1]
    return [[(piece.x + x_change, piece.y + y_change) for x_change in idx_changes
             if 1 <= piece.x + x_change <= 8 and 1 <= piece.y + y_change <= 8 and (x_change != 0 or y_change != 0)
             and (piece.x + x_change, piece.y + y_change) not in board.locations[color]]
            for y_change in idx_changes]


# get list of squares attacked by a pawn, taking into account other pieces on the board
def get_pawn_attacked_squares(board, piece):
    if not isinstance(piece, pawn.Pawn):
        return TypeError
    attacked_squares = []
    color = "white" if piece.color == "white" else "black"
    if 1 <= piece.x - 1 <= 8:
        if (piece.x - 1, piece.y + 1) not in board.locations[color]:
            attacked_squares.append((piece.x - 1, piece.y + 1))
    if 1 <= piece.x + 1 <= 8:
        if (piece.x - 1, piece.y + 1) not in board.locations[color]:
            attacked_squares.append((piece.x + 1, piece.y + 1))
    return attacked_squares


# get list of squares attacked by a knight, taking into account other pieces on the board
def get_knight_attacked_squares(board, piece):
    if not isinstance(piece, knight.Knight):
        return TypeError
    color = "white" if piece.color == "white" else "black"

    attacked_squares = [(piece.x - 2, piece.y - 1), (piece.x - 2, piece.y + 1),
                        (piece.x - 1, piece.y - 2), (piece.x - 1, piece.y + 2),
                        (piece.x + 1, piece.y - 2), (piece.x + 1, piece.y + 2),
                        (piece.x + 2, piece.y - 1), (piece.x + 2, piece.y + 1)]
    valid_moves = list(filter(lambda tup: 1 <= tup[0] <= 8 and 1 <= tup[1] <= 8 and tup not in board.locations[color],
                              attacked_squares))
    return valid_moves


# class to organize each instance of a chess board
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
        self.locations = {"white": {(piece.x, piece.y) for piece in self.white_pieces},  # a dict of sets of locations.
                          "black": {(piece.x, piece.y) for piece in self.black_pieces}}
        self.white_attacked_squares = self.get_attacked_squares()["white"]
        self.black_attacked_squares = self.get_attacked_squares()["black"]

    # get list of squares attacked by white and by black
    # use to check for Check and Checkmate
    def get_attacked_squares(self):
        white_attacked_squares = {}
        black_attacked_squares = {}
        for piece in self.white_pieces:
            white_attacked_squares[piece] = self.get_piece_attacked_squares(piece)
        for piece in self.black_pieces:
            black_attacked_squares[piece] = self.get_piece_attacked_squares(piece)
        return {"white": white_attacked_squares, "black": black_attacked_squares}

    # get list of squares attacked by a single piece, taking into account other pieces on the board
    # squares returned in chess notation
    def get_piece_attacked_squares(self, piece):
        if isinstance(piece, rook.Rook):
            return get_rook_attacked_squares(self, piece)
        elif isinstance(piece, bishop.Bishop):
            return get_bishop_attacked_squares(self, piece)
        elif isinstance(piece, queen.Queen):
            return get_rook_attacked_squares(self, piece).extend(get_bishop_attacked_squares(self, piece))
        elif isinstance(piece, king.King):
            return get_king_attacked_squares(self, piece)
        elif isinstance(piece, pawn.Pawn):
            return get_pawn_attacked_squares(self, piece)
        elif isinstance(piece, knight.Knight):
            return get_knight_attacked_squares(self, piece)
        else:
            return TypeError("input is not a Piece instance")

    # return current board score
    def get_score(self):
        return self.score

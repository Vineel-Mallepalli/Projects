from ChessProject.chess_pieces import queen, rook, pawn, bishop, knight, king

from collections import Counter

from ChessProject.chess_board import board


def get_counts(arr):
    # if not board.is_valid(arr):
    #     return AssertionError
    if arr == board.constants.START_BOARD:
        return board.constants.START_COUNTS
    # counter = board.constants.START_COUNTER
    counter = Counter()
    for row in range(len(arr)):
        for col in range(len(arr)):
            obj = arr[row][col]
            if obj == "":
                continue
            counter[board.type_to_str(obj)] += 1
    return counter


# test StartBoard
print(get_counts([[rook.Rook(1, 1, "black"), knight.Knight(2, 1, "black"), bishop.Bishop(3, 1, "black"),
                   queen.Queen(4, 1, "black"), king.King(5, 1, "black"), bishop.Bishop(6, 1, "black"),
                   knight.Knight(7, 1, "black"), rook.Rook(8, 1, "black")],
                  [pawn.Pawn(x + 1, 7, "black") for x in range(8)],
                  ["" for _ in range(8)], ["" for _ in range(8)], ["" for _ in range(8)], ["" for _ in range(8)],
                  [pawn.Pawn(x + 1, 2, "white") for x in range(8)],
                  [rook.Rook(1, 1, "white"), knight.Knight(2, 1, "white"), bishop.Bishop(3, 1, "white"),
                   queen.Queen(4, 1, "white"), king.King(5, 1, "white"), bishop.Bishop(6, 1, "white"),
                   knight.Knight(7, 1, "white"), rook.Rook(8, 1, "white")]]))

# test random board
print(get_counts([[pawn.Pawn(1, 2, "white"), queen.Queen(4, 1, "white"), bishop.Bishop(3, 1, "black"),
                   queen.Queen(4, 1, "black"), king.King(5, 1, "black"), queen.Queen(4, 1, "white"),
                   knight.Knight(7, 1, "black"), king.King(5, 1, "black")],
                  [rook.Rook(x + 1, 7, "black") for x in range(8)],
                  ["" for _ in range(8)], ["" for _ in range(8)], ["" for _ in range(8)], ["" for _ in range(8)],
                  [pawn.Pawn(x + 1, 2, "white") for x in range(8)],
                  [rook.Rook(1, 1, "white"), knight.Knight(2, 1, "white"), bishop.Bishop(3, 1, "white"),
                   queen.Queen(4, 1, "white"), king.King(5, 1, "white"), bishop.Bishop(6, 1, "white"),
                   knight.Knight(7, 1, "white"), pawn.Pawn(1, 2, "white")]]))

print(get_counts([[pawn.Pawn(1, 2, "white"), queen.Queen(4, 1, "white")], [bishop.Bishop(3, 1, "black"),
                                                                           queen.Queen(4, 1, "black")]]))

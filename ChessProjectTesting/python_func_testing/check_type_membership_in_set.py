from ChessProject.chess_pieces import pawn, rook, knight, bishop, queen, king, piece
from collections import Counter

print(["." for x in range(8)])
white_pieces = {rook.Rook(1, 1, "white"), knight.Knight(2, 1, "white"), bishop.Bishop(3, 1, "white"),
                queen.Queen(4, 1, "white"), king.King(5, 1, "white"), bishop.Bishop(6, 1, "white"),
                knight.Knight(7, 1, "white"), rook.Rook(8, 1, "white")}.union(
               {pawn.Pawn(x + 1, 2, "white") for x in range(8)})
print(white_pieces)

# is there some way to count how many of a type are in a set?
# use Counter. If 0, not in set.
counter = Counter()
for chess_piece in white_pieces:
    counter[type(chess_piece)] += 1
print(counter[type(pawn.Pawn(3, 1, "white"))])

# in code: have type to str function so we can use the str as key in counter.
print(isinstance(pawn.Pawn(3, 1, "white"), pawn.Pawn))
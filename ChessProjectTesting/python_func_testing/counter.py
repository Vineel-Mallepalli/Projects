from ChessProject.chess_pieces import pawn, rook, knight, bishop, queen, king, piece
from collections import Counter

white_pieces = {rook.Rook(1, 1, "white"), knight.Knight(2, 1, "white"), bishop.Bishop(3, 1, "white"),
                queen.Queen(4, 1, "white"), king.King(5, 1, "white"), bishop.Bishop(6, 1, "white"),
                knight.Knight(7, 1, "white"), rook.Rook(8, 1, "white")}.union(
               {pawn.Pawn(x + 1, 2, "white") for x in range(8)})

# Counter to count type of piece found in set
count_types = Counter()
for chess_piece in white_pieces:
    count_types[type(chess_piece)] += 1
print(count_types)

# DON'T USE! Alternate method: input set to Counter. Counts EACH object independently. BAD.
count_types2 = Counter(white_pieces)
print(count_types2)

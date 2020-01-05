from Chess.main.chess_pieces import queen, piece

# using type vs. isinstance to check exact type of piece
print(type(queen.Queen(3, 1, "white")) is queen.Queen)
print(type(queen.Queen(3, 1, "white")) is piece.Piece)
print(isinstance(queen.Queen(3, 1, "white"), queen.Queen))
print(isinstance(queen.Queen(3, 1, "white"), piece.Piece))

# based on results, choose to use type to ensure knowledge of exact piece type.

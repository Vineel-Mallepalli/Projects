from Chess.main.chess_pieces import knight, bishop, king, queen, pawn
from Chess.main.chess_pieces import rook

START_BOARD = [[rook.Rook(1, 8, "black"), knight.Knight(2, 8, "black"), bishop.Bishop(3, 8, "black"),
                queen.Queen(4, 8, "black"), king.King(5, 8, "black"), bishop.Bishop(6, 8, "black"),
                knight.Knight(7, 8, "black"), rook.Rook(8, 8, "black")],
               [pawn.Pawn(x + 1, 7, "black") for x in range(7)],
               ["" for _ in range(8)], ["" for _ in range(8)], ["" for _ in range(8)], ["" for _ in range(8)],
               [pawn.Pawn(x + 1, 2, "white") for x in range(7)],
               [rook.Rook(1, 1, "white"), knight.Knight(2, 1, "white"), bishop.Bishop(3, 1, "white"),
                queen.Queen(4, 1, "white"), king.King(5, 1, "white"), bishop.Bishop(6, 1, "white"),
                knight.Knight(7, 1, "white"), rook.Rook(8, 1, "white")]]

START_COUNTS = {"white": {"bishop": 2, "rook": 2, "knight": 2, "king": 1, "queen": 1, "pawn": 8},
                "black": {"bishop": 2, "rook": 2, "knight": 2, "king": 1, "queen": 1, "pawn": 8}}

START_PIECES = {rook.Rook(1, 8, "black"), knight.Knight(2, 8, "black"), bishop.Bishop(3, 8, "black"),
                queen.Queen(4, 8, "black"), king.King(5, 8, "black"), bishop.Bishop(6, 8, "black"),
                knight.Knight(7, 8, "black"), rook.Rook(8, 8, "black"),
                pawn.Pawn(1, 7, "black"), pawn.Pawn(2, 7, "black"), pawn.Pawn(3, 7, "black"), pawn.Pawn(4, 7, "black"),
                pawn.Pawn(5, 7, "black"), pawn.Pawn(6, 7, "black"), pawn.Pawn(7, 7, "black"), pawn.Pawn(8, 7, "black"),
                rook.Rook(1, 1, "white"), knight.Knight(2, 1, "white"), bishop.Bishop(3, 1, "white"),
                queen.Queen(4, 1, "white"), king.King(5, 1, "white"), bishop.Bishop(6, 1, "white"),
                knight.Knight(7, 1, "white"), rook.Rook(8, 1, "white"),
                pawn.Pawn(1, 2, "white"), pawn.Pawn(2, 2, "white"), pawn.Pawn(3, 2, "white"), pawn.Pawn(4, 2, "white"),
                pawn.Pawn(5, 2, "white"), pawn.Pawn(6, 2, "white"), pawn.Pawn(7, 2, "white"), pawn.Pawn(8, 2, "white"),
                }

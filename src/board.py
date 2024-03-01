from src.pieces import Piece


class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        # Initialize board with starting piece placements
        # (refer to "Fluent Python" for loop structures and data manipulation)
        for col in range(8):
            self.board[1][col] = Piece("black", "pawn", (1, col))
            self.board[6][col] = Piece("white", "pawn", (6, col))
            # Place other pieces (rooks, knights, bishops, queen, king)
            piece_type = ("rook", "knight", "bishop", "queen", "king")[col % 5]
            self.board[0][col] = Piece("black", piece_type, (0, col))
            self.board[7][col] = Piece("white", piece_type, (7, col))

    def update_board(self, new_square, piece_type, captured_piece=None):
        # Update board state after a valid move
        self.board[new_square[0]][new_square[1]] = piece_type
        # Implement logic for captured piece handling (if any)
        # (update captured piece position or remove it from the board)

    def get_piece_at(self, square):
        return self.board[square[0]][square[1]]


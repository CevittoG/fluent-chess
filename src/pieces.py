from typing import Tuple
from src.utils import cute_print


class Piece:
    def __init__(self, color: str, type: str, current_square: Tuple[int, int]):
        self.color = color
        self.type = type
        self.current_square = current_square
        self.has_moved = False

    # def move(self, new_square: Tuple[int, int], board: Board):
    #     # Validate move based on piece type and current board state
    #     # (implement logic based on specific piece rules)
    #     if self.is_valid_move(new_square, board):
    #         # Update piece position and board state
    #         self.current_square = new_square
    #         board.update_board(self.current_square, self.type, None)  # Placeholder for capturing logic
    #         # Handle special moves like castling or en passant if necessary

    def get_valid_moves(self, board) -> list:
        # Implement logic to check if the move is valid for the specific piece type. This will be overwritten by polymorphic behavior with subclasses (inherit)
        return []


class Pawn(Piece):
    def __init__(self, color, current_square):
        super().__init__(color, "pawn", current_square)

    def get_valid_moves(self, board) -> list:
        valid_moves = []
        row, col = self.current_square

        # Define standard pawn moves (one or two squares forward)
        if self.color == "white":
            move_direction = -1
        else:
            move_direction = 1

        # One square move
        if 0 <= row + move_direction < 8 and board.get_piece_at((row + move_direction, col)) is None:
            valid_moves.append((row + move_direction, col))

        # Two squares move (only for first move)
        if row == (6 if self.color == "white" else 1) and board.get_piece_at((row + move_direction, col)) is None and board.get_piece_at((row + 2 * move_direction, col)) is None:
            valid_moves.append((row + 2 * move_direction, col))

        # Capture right diagonal moves (if enemy piece is present)
        if 0 <= row + move_direction < 8 and 0 <= col + 1 < 8 and board.get_piece_at((row + move_direction, col + 1)) is not None and board.get_piece_at((row + move_direction, col + 1)).color != self.color:
            valid_moves.append((row + move_direction, col + 1))

        # Capture left diagonal moves (if enemy piece is present)
        if 0 <= row + move_direction < 8 and 0 <= col - 1 < 8 and board.get_piece_at((row + move_direction, col - 1)) is not None and board.get_piece_at((row + move_direction, col - 1)).color != self.color:
            valid_moves.append((row + move_direction, col - 1))

        return valid_moves

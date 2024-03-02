from src.pieces import Piece, King, Queen, Bishop, Knight, Rook, Pawn
from typing import Tuple, Union
from src.utils import cute_print


class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        # Initialize board with starting piece placements
        # (refer to "Fluent Python" for loop structures and data manipulation)
        for col in range(8):
            self.board[1][col] = Pawn("black", (1, col))
            self.board[6][col] = Pawn("white", (6, col))
        # Place other pieces
        positions = [(i, j) for i in range(8) for j in range(8)]
        for color, row in zip(("black", "white"), (0, 7)):
            for j, piece_type in enumerate([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
                self.board[row][j] = piece_type(color, positions[row * 8 + j])

    def get_piece_at(self, position: Tuple[int, int]) -> Union[Piece, None]:
        """
        Gets the piece at the specified position on the board.

        Args:
            position: A tuple (row, col) representing the board position.

        Returns:
            The piece object at the given position, or None if no piece is present.
        """
        row, col = position
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        else:
            return None

    def move_piece(self, start_position: Tuple[int, int], end_position: Tuple[int, int]):
        # Get the piece at the starting position
        piece = self.get_piece_at(start_position)

        # Check if there's a piece and the destination is valid (currently a placeholder)
        if piece is None:
            cute_print(f'There is no piece in position {start_position}', 'error', 'red')
        elif piece is not None and end_position not in piece.get_valid_moves(self):
            cute_print(f"{piece.color}_{piece.type} at {start_position} can't move to {end_position}", f'{piece.color}_{piece.type}', 'yellow')
        elif piece is not None and end_position in piece.get_valid_moves(self):
            # Update the piece state
            piece.has_moved = True
            piece.current_square = end_position
            # Update the board state
            self.board[start_position[0]][start_position[1]] = None
            self.board[end_position[0]][end_position[1]] = piece

            cute_print(f"{piece.color}_{piece.type}: {start_position} -> {end_position}", f'{piece.color}_{piece.type}')

    # def is_valid_move(self, piece, start_position, end_position):
    #     """
    #     Placeholder method to check if a move is valid (not implemented yet).
    #
    #     Args:
    #         piece: The piece object being moved.
    #         start_position: A tuple (row, col) representing the starting position.
    #         end_position: A tuple (row, col) representing the desired ending position.
    #
    #     Returns:
    #         True if the move is valid, False otherwise (currently always returns False).
    #     """
    #     return True  # Placeholder until actual validation is implemented

    # def update_board(self, new_square, piece: Piece, captured_piece=None):
    #     # Update board state after a valid move
    #     self.board[new_square[0]][new_square[1]] = piece
    #     # Implement logic for captured piece handling (if any)
    #     # (update captured piece position or remove it from the board)


from src.pieces import Piece, King, Queen, Bishop, Knight, Rook, Pawn
from typing import Tuple, Union
from src.utils import cute_print, find_position
import sys


class Square:
    def __init__(self, row, col):
        self.row = row
        self.col = col


class Board:
    def __init__(self):
        self.board: list[list] = [[None for _ in range(8)] for _ in range(8)]
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

    def get_all_pieces(self, filter_by: Union[None, Tuple] = None):
        filter_func, filter_value = filter_by or (lambda piece, _: piece is not None, None)  # Default to all pieces

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if filter_func(piece, filter_value):
                    yield piece

    def move_piece(self, piece, start_position: Tuple[int, int], end_position: Tuple[int, int], piece_valid_moves: list[tuple[tuple[int, int], str]]):
        # Check if there's a piece at start_position
        if piece is None:
            cute_print(f'There is no piece in position {start_position}', 'error', 'red')
        # Check if piece found can't move to end_position
        elif piece is not None and end_position not in piece_valid_moves:
            cute_print(f"{piece.color}_{piece.type} at {start_position} can't move to {end_position}", f'{piece.color}_{piece.type}', 'yellow')
        # Check if piece found can move to end_position
        elif piece is not None and end_position in piece_valid_moves:
            # Update the piece state
            piece.movements.append(end_position)
            piece.current_square = end_position
            # Update the board state
            self.board[start_position[0]][start_position[1]] = None
            # Check for Pawn promotion:
            if piece.type == 'pawn' and end_position[0] in (0, 7):
                self.board[end_position[0]][end_position[1]] = Queen(piece.color, end_position)  # ToDo: Choose a piece to promote to (queen, rook, bishop, knight)")
            else:
                self.board[end_position[0]][end_position[1]] = piece
            # Check King castling
            if piece.type == 'king' and end_position[0] in (0, 7):
                pass
            cute_print(f"{piece.color}_{piece.type}: {start_position} -> {end_position}", f'{piece.color}_{piece.type}')
        else:
            validated_end_position, move_label = find_position(piece_valid_moves, end_position)
            # Check if piece found can't move to end_position
            if not validated_end_position:
                cute_print(f"{piece.color}_{piece.type} at {start_position} can't move to {end_position}", f'{piece.color}_{piece.type}', 'yellow')
            # Check if piece found can move to end_position
            elif end_position == validated_end_position:
                self.perform_standard_move(piece, start_position, end_position)

                if isinstance(piece, Pawn) and end_position[0] in (0, 7):   # Pawn promotion
                    self.perform_promotion(piece, end_position)
                elif isinstance(piece, Pawn) and 'passant' in move_label:   # Pawn passing
                    self.perform_en_passant(piece, end_position)
                elif isinstance(piece, King) and 'castling' in move_label:  # King castling
                    self.perform_castling(start_position, end_position, move_label)

    def perform_standard_move(self, piece, start_position: tuple[int, int], end_position: tuple[int, int]):
        # Update the piece state
        piece.move(end_position)
        # Update the board state
        self.board[start_position[0]][start_position[1]] = None
        self.board[end_position[0]][end_position[1]] = piece
        cute_print(f"{piece.color}_{piece.type}: {start_position} -> {end_position}", f'{piece.color}_{piece.type}')

    def perform_promotion(self, piece: Pawn, end_position: tuple[int, int]):
        self.board[end_position[0]][end_position[1]] = Queen(piece.color, end_position)  # ToDo: Choose a piece to promote to (queen, rook, bishop, knight)")

    def perform_castling(self, start_position: tuple[int, int], end_position: tuple[int, int], move_label: str):
    def perform_en_passant(self, piece: Pawn, end_position: tuple[int, int]):
        pass

    def copy(self):
        """Creates a copy of the board.

        Returns:
            Board: A new Board object representing a copy of the current board.
        """

        new_board = Board()  # Create a new Board object
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                new_board.board[row][col] = piece if piece is not None else None
        return new_board

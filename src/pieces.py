from typing import Tuple, Union
from src.utils import cute_print


class Piece:
    def __init__(self, color: str, type: str, current_square: Tuple[int, int]):
        self.color: str = color
        self.type: str = type
        self.current_square: Tuple[int, int] = current_square
        self.movements: list[Tuple[int, int]] = [current_square]
        self.captured: list[Union[Piece, None]] = [None]

    def get_valid_moves(self, board) -> list:
        # Implement logic to check if the move is valid for the specific piece type. This will be overwritten by polymorphic behavior with subclasses (inherit)
        return []


class King(Piece):
    def __init__(self, color, current_square):
        super().__init__(color, "king", current_square)

    def get_valid_moves(self, board) -> list:
        valid_moves = []
        row, col = self.current_square

        # Get rows and cols around piece... Ej: white king at initial position (0, 7)
        min_row = max(0, row - 1)  # (0, 6) -> 6
        max_row = min(7, row + 1)  # (7, 8) -> 7
        min_col = max(0, col - 1)  # (0, 3) -> 3
        max_col = min(7, col + 1)  # (7, 5) -> 5

        # iterate over posible positions
        for new_row in range(min_row, max_row + 1):
            for new_col in range(min_col, max_col + 1):
                # Check if the square is empty or occupied by an enemy piece
                piece_at_destination = board.get_piece_at((new_row, new_col))
                if (new_row, new_col) != (row, col) and 0 <= new_row < 8 and 0 <= new_col < 8 and (piece_at_destination is None or piece_at_destination.color != self.color):
                    valid_moves.append((new_row, new_col))

        # Castling
        if len(self.movements) == 1 and not self.in_check(board):
            # Check for rook on both sides and their move status
            left_rook = board.get_piece_at((row, 0))
            right_rook = board.get_piece_at((row, 7))

            # Check for queen-side castling (left rook)
            if left_rook is not None and left_rook.color == self.color and len(left_rook.movements) == 1:
                # Check squares between king and rook are empty
                middle_piece = False
                for middle_col in range(1, col):
                    if board.get_piece_at((row, middle_col)) is not None:
                        middle_piece = True
                        break  # Stop if any piece is encountered
                if not middle_piece:
                    # Check if movement will put King on check
                    if not King(self.color, (row, col - 2)).in_check(board):
                        # Add queen-side castling move (king moves 2 left, rook jumps to position next to king)
                        valid_moves.append((row, col - 2))

            # Check for king-side castling (right rook)
            if right_rook is not None and right_rook.color == self.color and len(right_rook.movements) == 1:
                # Check squares between king and rook are empty
                middle_piece = False
                for middle_col in range(col + 1, 7):
                    if board.get_piece_at((row, middle_col)) is not None:
                        middle_piece = True
                        break  # Stop if any piece is encountered
                if not middle_piece:
                    # Check if movement will put King on check
                    if not King(self.color, (row, col + 2)).in_check(board):
                        # Add king-side castling move (king moves 2 right, rook jumps to position next to king)
                        valid_moves.append((row, col + 2))

        return valid_moves

    def in_check(self, board) -> bool:
        # Check for enemy pieces attacking the king's position
        king_row, king_col = self.current_square
        for row in range(8):
            for col in range(8):
                piece = board.get_piece_at((row, col))
                if piece is not None and piece.color != self.color and (king_row, king_col) in piece.get_valid_moves(board):
                    return True  # Enemy piece can capture the king
        return False


class Queen(Piece):
    def __init__(self, color, current_square):
        super().__init__(color, "queen", current_square)

    def get_valid_moves(self, board) -> list:
        valid_moves = []
        row, col = self.current_square

        # Define directions for movements
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        # Iterate through directions and check for valid moves
        for move_row, move_col in directions:
            new_row, new_col = row + move_row, col + move_col

            # Check if the move is within board limits
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                # Check if the square is empty or occupied by an enemy piece
                piece_at_destination = board.get_piece_at((new_row, new_col))

                # Stop validating that direction if friendly piece is found
                if piece_at_destination is not None and piece_at_destination.color == self.color:
                    break
                # Valid move if empty or enemy piece
                elif piece_at_destination is None:
                    valid_moves.append((new_row, new_col))
                # Stop iterating only if encountering an enemy piece
                elif piece_at_destination is not None and piece_at_destination.color != self.color:
                    valid_moves.append((new_row, new_col))
                    break
                # Continue iterating if empty square or friendly piece encountered
                new_row, new_col = new_row + move_row, new_col + move_col

        return valid_moves


class Bishop(Piece):
    def __init__(self, color, current_square):
        super().__init__(color, "bishop", current_square)

    def get_valid_moves(self, board) -> list:
        valid_moves = []
        row, col = self.current_square

        # Define directions for movements
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        # Iterate through directions and check for valid moves
        for move_row, move_col in directions:
            new_row, new_col = row + move_row, col + move_col

            # Check if the move is within board limits
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                # Check if the square is empty or occupied by an enemy piece
                piece_at_destination = board.get_piece_at((new_row, new_col))

                # Stop validating that direction if friendly piece is found
                if piece_at_destination is not None and piece_at_destination.color == self.color:
                    break
                # Valid move if empty or enemy piece
                elif piece_at_destination is None:
                    valid_moves.append((new_row, new_col))
                # Stop iterating only if encountering an enemy piece
                elif piece_at_destination is not None and piece_at_destination.color != self.color:
                    valid_moves.append((new_row, new_col))
                    break
                # Continue iterating if empty square or friendly piece encountered
                new_row, new_col = new_row + move_row, new_col + move_col

        return valid_moves


class Knight(Piece):
    def __init__(self, color, current_square):
        super().__init__(color, "knight", current_square)

    def get_valid_moves(self, board) -> list:
        valid_moves = []
        row, col = self.current_square

        # Define possible knight moves (in L-shape patterns)
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                        (1, 2), (1, -2), (-1, 2), (-1, -2)]

        # Iterate through potential moves and check validity
        for move_row, move_col in knight_moves:
            new_row, new_col = row + move_row, col + move_col

            # Check if the move is within board limits
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                # Check if the square is empty or occupied by an enemy piece
                piece_at_destination = board.get_piece_at((new_row, new_col))
                if piece_at_destination is None or piece_at_destination.color != self.color:
                    valid_moves.append((new_row, new_col))

        return valid_moves


class Rook(Piece):
    def __init__(self, color, current_square):
        super().__init__(color, "rook", current_square)

    def get_valid_moves(self, board) -> list:
        valid_moves = []
        row, col = self.current_square

        # Define directions for movements
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # Iterate through directions and check for valid moves
        for move_row, move_col in directions:
            new_row, new_col = row + move_row, col + move_col

            # Check if the move is within board limits
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                # Check if the square is empty or occupied by an enemy piece
                piece_at_destination = board.get_piece_at((new_row, new_col))

                # Stop validating that direction if friendly piece is found
                if piece_at_destination is not None and piece_at_destination.color == self.color:
                    break
                # Valid move if empty or enemy piece
                elif piece_at_destination is None:
                    valid_moves.append((new_row, new_col))
                # Stop iterating only if encountering an enemy piece
                elif piece_at_destination is not None and piece_at_destination.color != self.color:
                    valid_moves.append((new_row, new_col))
                    break
                # Continue iterating if empty square or friendly piece encountered
                new_row, new_col = new_row + move_row, new_col + move_col

        return valid_moves


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

        # One square move (could be a "Promotion")
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

        # Additional logic for "en passant" (in passing)
        passing_piece = board.get_piece_at((row, col + 1))
        if passing_piece is not None and passing_piece.color != self.color and len(passing_piece.movements) == 2:
            valid_moves.append((row + move_direction, col + 1))  # Capture en passant
        passing_piece = board.get_piece_at((row, col - 1))
        if passing_piece is not None and passing_piece.color != self.color and len(passing_piece.movements) == 2:
            valid_moves.append((row + move_direction, col - 1))  # Capture en passant

        return valid_moves

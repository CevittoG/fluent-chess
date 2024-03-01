from src import Board, Piece
import pygame
import pathlib

# Load piece images based on your file structure
IMG_DIRECTORY = pathlib.Path(__file__).absolute().parent.parent / 'images'
PIECES_NAMES = ('king', 'queen', 'bishop', 'knight', 'rook', 'pawn')
PIECES_COLORS = ('white', 'black')
PIECES_IMAGES = {f"{color}_{name}": pygame.image.load(str(IMG_DIRECTORY / f"{color}_{name}.png")) for color in PIECES_COLORS for name in PIECES_NAMES}

PIECE_IMG_SIZE = list(PIECES_IMAGES.values())[0].get_size()
BOARD_SIZE = 800
SQUARE_SIZE = BOARD_SIZE / 8


def calculate_piece_size(square_size):
    """
    Calculates the appropriate size for a piece image, maintaining aspect ratio.

    Args:
        square_size (int): The size of each square on the chessboard.
        piece_image (pygame.Surface): The original image of the chess piece.

    Returns:
        tuple: (scaled_width, scaled_height) of the piece image with maintained aspect ratio.
    """

    original_width, original_height = PIECE_IMG_SIZE

    # Calculate the maximum allowed size based on the square dimensions
    square_size *= 0.85
    max_size = min(square_size, original_width, original_height)

    # Maintain aspect ratio while scaling
    scale_factor = max_size / original_width
    scaled_width = int(original_width * scale_factor)
    scaled_height = int(original_height * scale_factor)

    return scaled_width, scaled_height


def draw_board(screen, board):
    """
    Iterates through each square on the board and draws a colored rectangle using pygame.draw.rect, alternating colors for a checkerboard pattern.
    :param screen:
    :param board:
    :return:
    """
    # Set colors for board squares
    light_square_color = (230, 220, 210)
    dark_square_color = (180, 170, 160)

    # Iterate over each square
    for row in range(8):
        for col in range(8):
            # Determine square color based on row and column parity
            square_color = light_square_color if (row + col) % 2 == 0 else dark_square_color

            # Create a rectangle representing the square
            square_rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

            # Fill the rectangle with the corresponding color
            pygame.draw.rect(screen, square_color, square_rect)


def draw_pieces(screen, board, piece_images):
    """
    Iterates through each square and checks if a piece is present. If so, it retrieves the piece image from a dictionary and uses pygame.blit to draw the image onto the corresponding square on the screen.
    :param screen:
    :param board:
    :param piece_images:
    :return:
    """
    square_size = screen.get_width() / 8
    piece_size = calculate_piece_size(square_size)

    # Iterate over each square on the board
    for row in range(8):
        for col in range(8):
            piece = board.get_piece_at((row, col))

            # If a piece is present, draw its image on the corresponding square
            if piece is not None:
                piece_image = piece_images[f"{piece.color}_{piece.type}"]
                # Scale the image (with appropriate filtering, if needed)
                scaled_piece_image = pygame.transform.scale(piece_image, piece_size)

                square_x = col * square_size
                square_y = row * square_size

                # Center the scaled piece image within the square
                piece_center_x = square_x + square_size / 2 - scaled_piece_image.get_width() / 2
                piece_center_y = square_y + square_size / 2 - scaled_piece_image.get_height() / 2

                # Draw the scaled piece at the calculated center position
                screen.blit(scaled_piece_image, (piece_center_x, piece_center_y))


def print_board(board):
    for row in board:
        for piece in row:
            if piece is None:
                print("·", end=" ")
            else:
                print(piece.color[0] + piece.type[0].upper(), end=" ")
        print()  # New line after each row

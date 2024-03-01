from src import Board, Piece
import pygame
import pathlib
from src.utils import cute_print

# Load piece images based on your file structure
IMG_DIRECTORY = pathlib.Path(__file__).absolute().parent.parent / 'images'
PIECES_NAMES = ('king', 'queen', 'bishop', 'knight', 'rook', 'pawn')
PIECES_COLORS = ('white', 'black')
PIECES_IMAGES = {f"{color}_{name}": pygame.image.load(str(IMG_DIRECTORY / f"{color}_{name}.png")) for color in PIECES_COLORS for name in PIECES_NAMES}

BOARD_PX_SIZE = 800
SQUARE_PX_SIZE = BOARD_PX_SIZE / 8
PIECE_PX_SIZE = list(PIECES_IMAGES.values())[0].get_size()

HIGHLIGHT_COLOR = (255, 200, 100)
SUCCESS_COLOR = (255, 200, 100)
ERROR_COLOR = (255, 200, 100)


def calculate_piece_size(square_size):
    """
    Calculates the appropriate size for a piece image, maintaining aspect ratio.

    Args:
        square_size (int): The size of each square on the chessboard.
        piece_image (pygame.Surface): The original image of the chess piece.

    Returns:
        tuple: (scaled_width, scaled_height) of the piece image with maintained aspect ratio.
    """

    original_width, original_height = PIECE_PX_SIZE

    # Calculate the maximum allowed size based on the square dimensions
    square_size *= 0.85
    max_size = min(square_size, original_width, original_height)

    # Maintain aspect ratio while scaling
    scale_factor = max_size / original_width
    scaled_width = int(original_width * scale_factor)
    scaled_height = int(original_height * scale_factor)

    return scaled_width, scaled_height


def draw_board(screen, board: Board):
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
            square_rect = pygame.Rect(col * SQUARE_PX_SIZE, row * SQUARE_PX_SIZE, SQUARE_PX_SIZE, SQUARE_PX_SIZE)

            # Fill the rectangle with the corresponding color
            pygame.draw.rect(screen, square_color, square_rect)


def draw_pieces(screen, board: Board, piece_images: dict, selected_piece_row: int, selected_piece_col: int):
    """
    Iterates through each square and checks if a piece is present. If so, it retrieves the piece image from a dictionary and uses pygame.blit to draw the image onto the corresponding square on the screen.
    :param screen:
    :param board:
    :param piece_images:
    :return:
    """
    piece_size = calculate_piece_size(SQUARE_PX_SIZE)

    # Iterate over each square on the board
    for row in range(8):
        for col in range(8):
            piece = board.get_piece_at((row, col))

            # Highlight the selected piece (if any)
            if row == selected_piece_row and col == selected_piece_col:

                # Create a rectangle representing the square
                square_rect = pygame.Rect(col * SQUARE_PX_SIZE, row * SQUARE_PX_SIZE, SQUARE_PX_SIZE, SQUARE_PX_SIZE)
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, square_rect, width=3)

            # If a piece is present, draw its image on the corresponding square
            if piece is not None:
                piece_image = piece_images[f"{piece.color}_{piece.type}"]
                # Scale the image (with appropriate filtering, if needed)
                scaled_piece_image = pygame.transform.scale(piece_image, piece_size)

                # Calculate piece image position based on mouse (if selected)
                if row == selected_piece_row and col == selected_piece_col:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    square_x = int(mouse_x // SQUARE_PX_SIZE) * SQUARE_PX_SIZE
                    square_y = int(mouse_y // SQUARE_PX_SIZE) * SQUARE_PX_SIZE

                else:
                    square_x = col * SQUARE_PX_SIZE
                    square_y = row * SQUARE_PX_SIZE

                # Center the scaled piece image within the square
                piece_center_x = square_x + SQUARE_PX_SIZE // 2 - scaled_piece_image.get_width() // 2
                piece_center_y = square_y + SQUARE_PX_SIZE // 2 - scaled_piece_image.get_height() // 2

                # Draw the scaled piece at the calculated center position
                screen.blit(scaled_piece_image, (piece_center_x, piece_center_y))


def print_board(board: Board):
    for row in board:
        for piece in row:
            if piece is None:
                print("·", end=" ")
            else:
                print(piece.color[0] + piece.type[0].upper(), end=" ")
        print()  # New line after each row

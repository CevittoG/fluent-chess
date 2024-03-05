from src import Board, Piece
import pygame
import pathlib
from src.utils import cute_print

MEDIA_DIRECTORY = pathlib.Path(__file__).absolute().parent.parent / 'media'

# Image settings
IMG_DIRECTORY = MEDIA_DIRECTORY / 'images'
PIECES_NAMES = ('king', 'queen', 'bishop', 'knight', 'rook', 'pawn')
PIECES_COLORS = ('white', 'black')
PIECES_IMAGES = {f"{color}_{name}": pygame.image.load(str(IMG_DIRECTORY / f"{color}_{name}.png")) for color in PIECES_COLORS for name in PIECES_NAMES}

# Font settings
FONT_DIRECTORY = MEDIA_DIRECTORY / 'fonts'
FONT_TTF_FILENAME = 'consola'  # 'micross' 'DMSans-Regular' 'verdana' 'Ubuntu-Regular'
FONT_TYPE = str(FONT_DIRECTORY / f'{FONT_TTF_FILENAME}.ttf')
FONT_SIZE = 20
SQUARE_FONT_SIZE = 10
FONT_COLOR = (255, 255, 255)  # (242, 242, 242)

# Icon Settings
ICON_DIRECTORY = MEDIA_DIRECTORY / 'icons'

# Board Measurements
BOARD_PX_SIZE = 800
SQUARE_PX_SIZE = BOARD_PX_SIZE // 8
BOARD_MARGIN = SQUARE_PX_SIZE // 2
PIECE_PX_SIZE = list(PIECES_IMAGES.values())[0].get_size()

# Colors
BACKGROUND_COLOR = (40, 40, 40)  # (58, 58, 58)
BOARD_LIGHT_COLOR = (247, 243, 235)
BOARD_DARK_COLOR = (158, 122, 91)
HIGHLIGHT_COLOR = (255, 215, 0)
POSSIBLE_MOVES_COLOR = (102, 187, 106)  # (153, 204, 0) or (139, 172, 139)
POSSIBLE_CAPTURES_COLOR = (204, 0, 0)


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


def draw_board(screen):
    """
    Iterates through each square on the board and draws a colored rectangle using pygame.draw.rect, alternating colors for a checkerboard pattern.
    :param screen:
    :param font:
    :return:
    """
    font = pygame.font.Font(FONT_TYPE, SQUARE_PX_SIZE // 10)
    # Iterate over each square
    for row in range(8):
        for col in range(8):
            # Determine square color based on row and column parity
            square_color = BOARD_LIGHT_COLOR if (row + col) % 2 == 0 else BOARD_DARK_COLOR
            # Create a rectangle representing the square
            square_rect = pygame.Rect(col * SQUARE_PX_SIZE + BOARD_MARGIN, row * SQUARE_PX_SIZE + BOARD_MARGIN, SQUARE_PX_SIZE, SQUARE_PX_SIZE)
            # Fill the rectangle with the corresponding color
            pygame.draw.rect(screen, square_color, square_rect)

            if col == 0:
                # Determine text color based on row and column parity
                text_color = BOARD_DARK_COLOR if (row + col) % 2 == 0 else BOARD_LIGHT_COLOR

                # Row numbers
                row_number = font.render(str(row + 1), True, text_color)  # Convert number to string
                row_number_position = (col * SQUARE_PX_SIZE + SQUARE_FONT_SIZE // 5 + BOARD_MARGIN, row * SQUARE_PX_SIZE + SQUARE_PX_SIZE - SQUARE_FONT_SIZE * 2 + BOARD_MARGIN)
                screen.blit(row_number, row_number_position)

                # Col letters
                col_letter = font.render(chr(ord('A') + row), True, text_color)
                col_letter_position = (row * SQUARE_PX_SIZE + SQUARE_PX_SIZE - SQUARE_FONT_SIZE * 2 + BOARD_MARGIN, col * SQUARE_PX_SIZE + SQUARE_FONT_SIZE // 5 + BOARD_MARGIN)
                screen.blit(col_letter, col_letter_position)


def draw_pieces(screen, board: Board, piece_images: dict, selected_piece_row: int, selected_piece_col: int):
    """
    Iterates through each square and checks if a piece is present. If so, it retrieves the piece image from a dictionary and uses pygame.blit to draw the image onto the corresponding square on the screen.
    :param screen:
    :param board:
    :param piece_images:
    :param selected_piece_row:
    :param selected_piece_col:
    :return:
    """
    piece_size = calculate_piece_size(int(SQUARE_PX_SIZE))

    # Iterate over each square on the board
    for row in range(8):
        for col in range(8):
            piece = board.get_piece_at((row, col))

            # Highlight the selected piece (if any)
            if row == selected_piece_row and col == selected_piece_col:
                # Create a rectangle representing the square
                highlight_square(screen, [(row, col)], HIGHLIGHT_COLOR)

            # If a piece is present, draw its image on the corresponding square
            if piece is not None:
                piece_image = piece_images[f"{piece.color}_{piece.type}"]
                # Scale the image (with appropriate filtering, if needed)
                scaled_piece_image = pygame.transform.scale(piece_image, piece_size)

                # Calculate piece image position based on mouse (if selected)
                if row == selected_piece_row and col == selected_piece_col:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    square_x = ((mouse_x - BOARD_MARGIN) // SQUARE_PX_SIZE) * SQUARE_PX_SIZE
                    square_y = ((mouse_y - BOARD_MARGIN) // SQUARE_PX_SIZE) * SQUARE_PX_SIZE

                else:
                    square_x = col * SQUARE_PX_SIZE
                    square_y = row * SQUARE_PX_SIZE

                # Center the scaled piece image within the square
                piece_center_x = square_x + SQUARE_PX_SIZE // 2 - scaled_piece_image.get_width() // 2 + BOARD_MARGIN
                piece_center_y = square_y + SQUARE_PX_SIZE // 2 - scaled_piece_image.get_height() // 2 + BOARD_MARGIN

                # Draw the scaled piece at the calculated center position
                screen.blit(scaled_piece_image, (piece_center_x, piece_center_y))


def highlight_square(screen, valid_moves: list[tuple], color: tuple[int, int, int]):
    """
    Highlights squares representing valid moves for the given piece.

    Args:
        screen:
        valid_moves:
        color:
    """
    for row, col in valid_moves:
        # Create a rectangle representing the square
        square_rect = pygame.Rect(col * SQUARE_PX_SIZE + BOARD_MARGIN, row * SQUARE_PX_SIZE + BOARD_MARGIN, SQUARE_PX_SIZE, SQUARE_PX_SIZE)
        pygame.draw.rect(screen, color, square_rect, width=8)


def render_players_info(screen, font: pygame.font.Font):
    # Black Player
    black_text = font.render('B:', True, FONT_COLOR)
    black_text_position = (BOARD_MARGIN, (BOARD_MARGIN - FONT_SIZE) // 2)
    screen.blit(black_text, black_text_position)

    black_c_text = font.render('Captured:', True, FONT_COLOR)
    black_c_text_position = (BOARD_MARGIN + SQUARE_PX_SIZE * 3, (BOARD_MARGIN - FONT_SIZE) // 2)
    screen.blit(black_c_text, black_c_text_position)

    # White Player
    white_text = font.render('W:', True, FONT_COLOR)
    white_text_position = (BOARD_MARGIN, BOARD_PX_SIZE + BOARD_MARGIN + ((BOARD_MARGIN - FONT_SIZE) // 2))
    screen.blit(white_text, white_text_position)

    white_c_text = font.render('Captured:', True, FONT_COLOR)
    white_c_text_position = (BOARD_MARGIN + SQUARE_PX_SIZE * 3, BOARD_PX_SIZE + BOARD_MARGIN + ((BOARD_MARGIN - FONT_SIZE) // 2))
    screen.blit(white_c_text, white_c_text_position)

from src import Board, Piece, GameState
import pygame
import pathlib
from src.utils import cute_print, position_to_chess_notation, move_to_chess_notation
from typing import Generator, Any

# Board Measurements
BOARD_PX_SIZE = 800
SQUARE_PX_SIZE = BOARD_PX_SIZE // 8
BOARD_MARGIN = SQUARE_PX_SIZE // 2

MEDIA_DIRECTORY = pathlib.Path(__file__).absolute().parent.parent / 'media'

# Image settings
IMG_DIRECTORY = MEDIA_DIRECTORY / 'images'
PIECES_NAMES = ('king', 'queen', 'bishop', 'knight', 'rook', 'pawn')
PIECES_COLORS = ('white', 'black')
PIECES_IMAGES = {f"{color}_{name}": pygame.image.load(str(IMG_DIRECTORY / f"{color}_{name}.png")) for color in PIECES_COLORS for name in PIECES_NAMES}
PIECE_PX_SIZE = list(PIECES_IMAGES.values())[0].get_size()

# Font settings
FONT_DIRECTORY = MEDIA_DIRECTORY / 'fonts'
FONT_TTF_FILENAME = 'consola'  # 'micross' 'DMSans-Regular' 'verdana' 'Ubuntu-Regular'
FONT_TYPE = str(FONT_DIRECTORY / f'{FONT_TTF_FILENAME}.ttf')
FONT_SIZE = BOARD_MARGIN // 3
SQUARE_FONT_SIZE = FONT_SIZE // 2
FONT_COLOR = (255, 255, 255)  # (242, 242, 242)

# Icon Settings
ICON_DIRECTORY = MEDIA_DIRECTORY / 'icons'
ICON_NAMES = ('king', 'queen', 'bishop', 'knight', 'rook', 'pawn', 'castling', 'promotion', 'sword', 'chess-clock')
ICONS = {f"{name}": pygame.image.load(str(ICON_DIRECTORY / f"{name}.png")) for name in ICON_NAMES}
ICON_PX_SIZE = list(ICONS.values())[0].get_size()

# Colors
BACKGROUND_COLOR = (40, 40, 40)  # (58, 58, 58)
BOARD_LIGHT_COLOR = (247, 243, 235)
BOARD_DARK_COLOR = (158, 122, 91)
HIGHLIGHT_COLOR = (255, 215, 0)
POSSIBLE_MOVES_COLOR = (102, 187, 106)  # (153, 204, 0) or (139, 172, 139)
POSSIBLE_CAPTURES_COLOR = (204, 0, 0)


def calculate_piece_size():
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
    max_size = min(SQUARE_PX_SIZE * 0.85, original_width, original_height)

    # Maintain aspect ratio while scaling
    scale_factor = max_size / original_width
    scaled_width = int(original_width * scale_factor)
    scaled_height = int(original_height * scale_factor)

    return scaled_width, scaled_height


def calculate_icon_size():
    original_width, original_height = ICON_PX_SIZE

    # Calculate the maximum allowed size based on the margin dimensions
    max_size = min(BOARD_MARGIN * 0.5, original_width, original_height)

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
    font = pygame.font.Font(FONT_TYPE, SQUARE_FONT_SIZE)  # SQUARE_PX_SIZE // 10)
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
                row_number = font.render(str(8 - row), True, text_color)  # Convert number to string
                row_number_position = (col * SQUARE_PX_SIZE + SQUARE_FONT_SIZE // 5 + BOARD_MARGIN, row * SQUARE_PX_SIZE + SQUARE_PX_SIZE - SQUARE_FONT_SIZE * 2 + BOARD_MARGIN)
                screen.blit(row_number, row_number_position)

                # Col letters
                col_letter = font.render(chr(ord('A') + row), True, text_color)
                col_letter_position = (row * SQUARE_PX_SIZE + SQUARE_PX_SIZE - SQUARE_FONT_SIZE * 2 + BOARD_MARGIN, col * SQUARE_PX_SIZE + SQUARE_FONT_SIZE // 5 + BOARD_MARGIN)
                screen.blit(col_letter, col_letter_position)


def draw_pieces(screen, board: Board, selected_piece_row: int, selected_piece_col: int):
    """
    Iterates through each square and checks if a piece is present. If so, it retrieves the piece image from a dictionary and uses pygame.blit to draw the image onto the corresponding square on the screen.
    :param screen:
    :param board:
    :param piece_images:
    :param selected_piece_row:
    :param selected_piece_col:
    :return:
    """
    piece_size = calculate_piece_size()

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
                piece_image = PIECES_IMAGES[f"{piece.color}_{piece.type}"]
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


def render_players_info(screen, font: pygame.font.Font, game: GameState):
    def get_data_from_log(log_data: list[dict], player_color: str, icon_size: tuple) -> tuple[pygame.Surface, str, list[pygame.Surface]]:
        p_data = [data for data in log_data if data['Player']['Color'] == player_color]

        if len(p_data) < 1:
            return pygame.Surface((0, 0)), '', []

        # Last piece moved
        last_move = p_data[-1]['Move']
        last_move_piece_icon = ICONS[f"{last_move['Piece'].lower()}"]
        scaled_piece_icon = pygame.transform.scale(last_move_piece_icon, icon_size)

        # Chess notation for last move
        last_move_position = move_to_chess_notation(last_move['Piece'], last_move['StartPosition'], last_move['EndPosition'], capture=last_move['Captured'], special_move=last_move['Special'])

        # Pieces captured by player_color
        captured_pieces_names = (turn['Move']['Captured'] for turn in p_data if turn['Move']['Captured'] is not False)
        captured_pieces = [pygame.transform.scale(ICONS[cp_name.lower()], icon_size) for cp_name in captured_pieces_names]

        return scaled_piece_icon, last_move_position, captured_pieces

    for player in ('Black', 'White'):
        icon_size = calculate_icon_size()
        # Get player data
        last_p_moved, last_position, captured_icon_list = get_data_from_log(game.log, player, icon_size)

        # Prepare player text
        text_position_y = (BOARD_MARGIN - FONT_SIZE) // 2
        text_position_y += BOARD_PX_SIZE + BOARD_MARGIN if player == 'White' else 0
        # Player initial letter
        player_text = font.render(f"{player[0]}:", True, FONT_COLOR)
        screen.blit(player_text, (BOARD_MARGIN, text_position_y))
        # Piece moved icon
        icon_position_y = (BOARD_MARGIN - FONT_SIZE) // 3
        icon_position_y += BOARD_PX_SIZE + BOARD_MARGIN if player == 'White' else 0
        screen.blit(last_p_moved, (BOARD_MARGIN + FONT_SIZE*2, icon_position_y))
        # Coordinates
        position_text = font.render(f"{last_position}", True, FONT_COLOR)
        screen.blit(position_text, (BOARD_MARGIN + FONT_SIZE*3 + icon_size[0], text_position_y))

        # ToDo: Clock... time played by player

        # Prepare captured icons
        sword_icon = pygame.transform.scale(ICONS['sword'], icon_size)
        sword_icon_position = (BOARD_MARGIN + SQUARE_PX_SIZE * 3, icon_position_y)
        screen.blit(sword_icon, sword_icon_position)
        # Icons iteration
        for i in range(len(captured_icon_list)):
            screen.blit(captured_icon_list[i], (sword_icon_position[0] + icon_size[0] * (i + 2), icon_position_y))


def render_square_info(screen, board):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    row = ((mouse_y - BOARD_MARGIN) // SQUARE_PX_SIZE)
    col = ((mouse_x - BOARD_MARGIN) // SQUARE_PX_SIZE)

    if 0 <= row < 8 and 0 <= col < 8:
        piece = board.get_piece_at((row, col))
        piece_type = f': {piece.type.title()}' if piece is not None else ''
        square = position_to_chess_notation((row, col))

        mouse_text = f'{square}{piece_type}'
        rect_diff = len(mouse_text) + 1 if len(mouse_text) == 2 else len(mouse_text) - 2  # ToDo: name could be better

        font = pygame.font.Font(FONT_TYPE, FONT_SIZE)

        # Rectangle
        square_rect = pygame.Rect(mouse_x, mouse_y, FONT_SIZE * rect_diff, FONT_SIZE * 1.5)
        pygame.draw.rect(screen, BACKGROUND_COLOR, square_rect, border_radius=8)

        # Text
        square_text = font.render(f"{mouse_text}", True, FONT_COLOR)
        screen.blit(square_text, (mouse_x + FONT_SIZE, mouse_y + FONT_SIZE * 0.25))

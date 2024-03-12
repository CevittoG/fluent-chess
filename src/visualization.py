from src import Board, GameState
from src.utils import position_to_chess_notation, move_to_chess_notation, seconds_to_hms
from src.config import update_game_dimensions, ICONS, ICON_PX_SIZE, FONT_TYPE, FONT_COLOR, PIECES_IMAGES, PIECE_PX_SIZE, BACKGROUND_COLOR, BOARD_LIGHT_COLOR, BOARD_DARK_COLOR, HIGHLIGHT_COLOR
import pygame
import math


def calculate_piece_size(screen: pygame.Surface):
    _, SQUARE_PX_SIZE, _, _, _, _ = update_game_dimensions(screen.get_width())

    original_width, original_height = PIECE_PX_SIZE

    # Calculate the maximum allowed size based on the square dimensions
    max_size = min(SQUARE_PX_SIZE * 0.85, original_width, original_height)

    # Maintain aspect ratio while scaling
    scale_factor = max_size / original_width
    scaled_width = int(original_width * scale_factor)
    scaled_height = int(original_height * scale_factor)

    return scaled_width, scaled_height


def calculate_icon_size(screen: pygame.Surface):
    _, _, MARGIN_PX_SIZE, _, _, _ = update_game_dimensions(screen.get_width())

    original_width, original_height = ICON_PX_SIZE

    # Calculate the maximum allowed size based on the margin dimensions
    max_size = min(MARGIN_PX_SIZE * 0.5, original_width, original_height)

    # Maintain aspect ratio while scaling
    scale_factor = max_size / original_width
    scaled_width = int(original_width * scale_factor)
    scaled_height = int(original_height * scale_factor)

    return scaled_width, scaled_height


def draw_board(screen: pygame.Surface):
    _, SQUARE_PX_SIZE, MARGIN_PX_SIZE, _, _, FONT_PX_SIZE_S = update_game_dimensions(screen.get_width())

    font = pygame.font.Font(FONT_TYPE, FONT_PX_SIZE_S)  # SQUARE_PX_SIZE // 10)
    # Iterate over each square
    for row in range(8):
        for col in range(8):
            # Determine square color based on row and column parity
            square_color = BOARD_LIGHT_COLOR if (row + col) % 2 == 0 else BOARD_DARK_COLOR
            # Create a rectangle representing the square
            square_rect = pygame.Rect(col * SQUARE_PX_SIZE + MARGIN_PX_SIZE, row * SQUARE_PX_SIZE + MARGIN_PX_SIZE, SQUARE_PX_SIZE, SQUARE_PX_SIZE)
            # Fill the rectangle with the corresponding color
            pygame.draw.rect(screen, square_color, square_rect)

            if col == 0:
                # Determine text color based on row and column parity
                text_color = BOARD_DARK_COLOR if (row + col) % 2 == 0 else BOARD_LIGHT_COLOR

                # Row numbers
                row_number = font.render(str(8 - row), True, text_color)  # Convert number to string
                row_number_position = (col * SQUARE_PX_SIZE + FONT_PX_SIZE_S // 5 + MARGIN_PX_SIZE, row * SQUARE_PX_SIZE + SQUARE_PX_SIZE - FONT_PX_SIZE_S * 2 + MARGIN_PX_SIZE)
                screen.blit(row_number, row_number_position)

                # Col letters
                col_letter = font.render(chr(ord('A') + row), True, text_color)
                col_letter_position = (row * SQUARE_PX_SIZE + SQUARE_PX_SIZE - FONT_PX_SIZE_S * 2 + MARGIN_PX_SIZE, col * SQUARE_PX_SIZE + FONT_PX_SIZE_S // 5 + MARGIN_PX_SIZE)
                screen.blit(col_letter, col_letter_position)


def draw_pieces(screen: pygame.Surface, board: Board, selected_piece_row: int, selected_piece_col: int):
    _, SQUARE_PX_SIZE, MARGIN_PX_SIZE, _, _, _ = update_game_dimensions(screen.get_width())

    piece_size = calculate_piece_size(screen)

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
                    square_x = ((mouse_x - MARGIN_PX_SIZE) // SQUARE_PX_SIZE) * SQUARE_PX_SIZE
                    square_y = ((mouse_y - MARGIN_PX_SIZE) // SQUARE_PX_SIZE) * SQUARE_PX_SIZE

                else:
                    square_x = col * SQUARE_PX_SIZE
                    square_y = row * SQUARE_PX_SIZE

                # Center the scaled piece image within the square
                piece_center_x = square_x + SQUARE_PX_SIZE // 2 - scaled_piece_image.get_width() // 2 + MARGIN_PX_SIZE
                piece_center_y = square_y + SQUARE_PX_SIZE // 2 - scaled_piece_image.get_height() // 2 + MARGIN_PX_SIZE

                # Draw the scaled piece at the calculated center position
                screen.blit(scaled_piece_image, (piece_center_x, piece_center_y))


def highlight_square(screen: pygame.Surface, valid_moves: list[tuple], color: tuple[int, int, int]):
    _, SQUARE_PX_SIZE, MARGIN_PX_SIZE, _, _, _ = update_game_dimensions(screen.get_width())

    for row, col in valid_moves:
        # Create a rectangle representing the square
        square_rect = pygame.Rect(col * SQUARE_PX_SIZE + MARGIN_PX_SIZE, row * SQUARE_PX_SIZE + MARGIN_PX_SIZE, SQUARE_PX_SIZE, SQUARE_PX_SIZE)
        pygame.draw.rect(screen, color, square_rect, width=SQUARE_PX_SIZE//10)


def render_players_info(screen: pygame.Surface, game: GameState):
    BOARD_PX_SIZE, SQUARE_PX_SIZE, MARGIN_PX_SIZE, _, FONT_PX_SIZE_M, _ = update_game_dimensions(screen.get_width())

    def get_data_from_log(log_data: list[dict], player_color: str) -> tuple[pygame.Surface, str, list[pygame.Surface]]:
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

    icon_size = calculate_icon_size(screen)
    font = pygame.font.Font(FONT_TYPE, FONT_PX_SIZE_M)

    for player in ('Black', 'White'):
        # Get player data
        icon_p_moved, chess_notation_move, captured_icon_list = get_data_from_log(game.log, player)

        # Prepare player text
        text_position_y = FONT_PX_SIZE_M
        text_position_y += BOARD_PX_SIZE + MARGIN_PX_SIZE if player == 'White' else 0
        # Player initial letter
        player_name = str(game.white_player) if player == 'White' else str(game.black_player)
        player_text = font.render(f"{player_name}", True, FONT_COLOR)
        screen.blit(player_text, (MARGIN_PX_SIZE, text_position_y))

        # Piece moved icon
        icon_moved_position_y = icon_size[0] // 2
        icon_moved_position_y += BOARD_PX_SIZE + MARGIN_PX_SIZE if player == 'White' else 0
        screen.blit(icon_p_moved, (MARGIN_PX_SIZE + (SQUARE_PX_SIZE * 1.5), icon_moved_position_y))
        # Coordinates
        move_text = font.render(f"{chess_notation_move}", True, FONT_COLOR)
        screen.blit(move_text, (MARGIN_PX_SIZE + (SQUARE_PX_SIZE * 1.5) + icon_size[0]*2, text_position_y))

        # Prepare captured icons
        for i in range(len(captured_icon_list)):
            # icons position over and under general clock
            icon_captured_position_y = MARGIN_PX_SIZE + SQUARE_PX_SIZE * 4
            icon_captured_position_y += icon_size[0]*2 if player == 'White' else -(icon_size[0]*3)
            icon_captured_position_y += (math.floor(i/2) * icon_size[0] * 1.5) if player == 'White' else -(math.floor(i/2) * icon_size[0] * 1.5)
            # icons positions on two columns
            icon_captured_position_x = MARGIN_PX_SIZE + BOARD_PX_SIZE + FONT_PX_SIZE_M
            icon_captured_position_x += 0 if (i % 2) == 0 else icon_size[0] * 2
            screen.blit(captured_icon_list[i], (icon_captured_position_x, icon_captured_position_y))


def render_square_info(screen: pygame.Surface, board):
    _, SQUARE_PX_SIZE, MARGIN_PX_SIZE, _, FONT_PX_SIZE_M, _ = update_game_dimensions(screen.get_width())

    mouse_x, mouse_y = pygame.mouse.get_pos()
    row = ((mouse_y - MARGIN_PX_SIZE) // SQUARE_PX_SIZE)
    col = ((mouse_x - MARGIN_PX_SIZE) // SQUARE_PX_SIZE)

    if 0 <= row < 8 and 0 <= col < 8:
        piece = board.get_piece_at((row, col))
        piece_type = f': {piece.type.title()}' if piece is not None else ''
        square = position_to_chess_notation((row, col))

        mouse_text = f'{square}{piece_type}'
        rect_multiplier = len(mouse_text) + 1 if len(mouse_text) == 2 else len(mouse_text) - 2

        font = pygame.font.Font(FONT_TYPE, FONT_PX_SIZE_M)

        # Rectangle
        square_rect = pygame.Rect(mouse_x, mouse_y, FONT_PX_SIZE_M * rect_multiplier, FONT_PX_SIZE_M * 1.5)
        pygame.draw.rect(screen, BACKGROUND_COLOR, square_rect, border_radius=8)

        # Text
        square_text = font.render(f"{mouse_text}", True, FONT_COLOR)
        screen.blit(square_text, (mouse_x + FONT_PX_SIZE_M, mouse_y + FONT_PX_SIZE_M * 0.25))


def render_clock(screen: pygame.Surface, game: GameState):
    BOARD_PX_SIZE, SQUARE_PX_SIZE, MARGIN_PX_SIZE, FONT_PX_SIZE_L, FONT_PX_SIZE_M, _ = update_game_dimensions(screen.get_width())

    x_position = MARGIN_PX_SIZE + BOARD_PX_SIZE + FONT_PX_SIZE_M
    # General Clock
    general_clock_font = pygame.font.Font(FONT_TYPE, FONT_PX_SIZE_L)
    general_clock_time = general_clock_font.render(f"{seconds_to_hms(game.time)}", True, FONT_COLOR)
    screen.blit(general_clock_time, (x_position, MARGIN_PX_SIZE + (SQUARE_PX_SIZE * 4) - FONT_PX_SIZE_L // 2))

    # Players Clock
    player_clock_font = pygame.font.Font(FONT_TYPE, FONT_PX_SIZE_M)
    # White
    wp_clock_time = player_clock_font.render(f"{seconds_to_hms(game.white_player.time)}", True, FONT_COLOR)
    screen.blit(wp_clock_time, (x_position, MARGIN_PX_SIZE + BOARD_PX_SIZE - FONT_PX_SIZE_M))
    # Black
    bp_clock_time = player_clock_font.render(f"{seconds_to_hms(game.black_player.time)}", True, FONT_COLOR)
    screen.blit(bp_clock_time, (x_position, MARGIN_PX_SIZE))

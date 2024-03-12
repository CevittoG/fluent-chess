import pygame
from pygame.locals import FULLSCREEN, RESIZABLE
from src import GameState, Board
from src.visualization import draw_board, draw_pieces, highlight_square, render_players_info, render_square_info, render_clock
from src.config import update_game_dimensions, ASPECT_RATIO, BACKGROUND_COLOR, POSSIBLE_MOVES_COLOR, POSSIBLE_CAPTURES_COLOR
from src.utils import Emoji, cute_print


def main():
    SEL_PIECE = None  # Stores the currently selected piece (None if no piece is selected)
    SEL_PIECE_ROW = None  # Row index of the selected piece (None if no piece is selected)
    SEL_PIECE_COL = None  # Column index of the selected piece (None if no piece is selected)
    mouse_is_down = False  # Flag to track mouse button state (pressed or released)

    # Initialize Pygame
    cute_print('Game started', 'rocket')
    pygame.init()

    # Set screen size and caption
    screen = pygame.display.set_mode((1200, 675), RESIZABLE)
    SCREEN_PX_W, SCREEN_PX_H = screen.get_width(), screen.get_height()
    BOARD_PX_SIZE, SQUARE_PX_SIZE, MARGIN_PX_SIZE, FONT_PX_SIZE_L, FONT_PX_SIZE_M, FONT_PX_SIZE_S = update_game_dimensions(SCREEN_PX_W)
    pygame.display.set_caption(f"Fluent Chess {Emoji('snake')}")
    game_font = pygame.font.Font(FONT_TYPE, FONT_PX_SIZE_M)

    # Create a game classes
    chessboard = Board()
    game = GameState(chessboard, None, None)  # ToDo: Create input for players names

    # (Optional) Initialize other game elements (e.g., AI, player information)

    # Main game loop
    valid_moves = []
    game.start()
    while game.state == 'running':
        game.update_elapsed_time()
        # Handle user input (e.g., mouse clicks for move selection)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.stop()

            # Resize event
            elif event.type == pygame.VIDEORESIZE:
                # Update screen size based on event
                screen_width, screen_height = event.w, event.h

                # Calculate new dimensions based on aspect ratio
                if screen_width / screen_height > ASPECT_RATIO:
                    new_width = int(screen_height * ASPECT_RATIO)
                    screen = pygame.display.set_mode((new_width, screen_height), RESIZABLE)
                    print(new_width, screen_height)
                else:
                    new_height = int(screen_width / ASPECT_RATIO)
                    screen = pygame.display.set_mode((screen_width, new_height), RESIZABLE)
                    print(screen_width, new_height)

                # Recalculate board and element sizes based on new screen size
                # update_game_dimensions(screen_width, screen_height)
                # Clear the screen before redrawing
                screen.fill(BACKGROUND_COLOR)

            # Click event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_is_down = True
                # Check if a piece is clicked within the board area
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row = (mouse_y - MARGIN_PX_SIZE) // SQUARE_PX_SIZE
                col = (mouse_x - MARGIN_PX_SIZE) // SQUARE_PX_SIZE

                if 0 <= row < 8 and 0 <= col < 8:
                    SEL_PIECE = chessboard.get_piece_at((row, col))
                    SEL_PIECE_ROW = row
                    SEL_PIECE_COL = col

                    # Check posible moves for specific piece
                    valid_moves = SEL_PIECE.get_valid_moves(chessboard) if SEL_PIECE is not None else []

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_is_down = False
                # Check if a piece is released on a valid square
                if SEL_PIECE is not None:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    new_row = (mouse_y - MARGIN_PX_SIZE) // SQUARE_PX_SIZE
                    new_col = (mouse_x - MARGIN_PX_SIZE) // SQUARE_PX_SIZE

                    # Handle piece movement
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        # Move piece on board and update states
                        game.turn((SEL_PIECE_ROW, SEL_PIECE_COL), (new_row, new_col), valid_moves)

                    # Reset selected piece information
                    SEL_PIECE = None
                    SEL_PIECE_ROW = None
                    SEL_PIECE_COL = None
                    valid_moves = []

        # (Optional) Perform AI move calculation (if applicable)

        # Render the game state (board, pieces, etc.)
        # Set background color
        screen.fill(BACKGROUND_COLOR)
        # Light and dark squares
        draw_board(screen)
        # Posible moves
        highlight_square(screen, [position for position, label in valid_moves if 'empty' in label], POSSIBLE_MOVES_COLOR)
        highlight_square(screen, [position for position, label in valid_moves if 'opponent' in label], POSSIBLE_CAPTURES_COLOR)
        # Every piece in the board
        draw_pieces(screen, chessboard, SEL_PIECE_ROW, SEL_PIECE_COL)
        # Square information flowing mouse position
        render_square_info(screen, chessboard)
        # Players info
        render_players_info(screen, game_font, game)
        # Time
        render_clock(screen, game)

        # Update the display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()

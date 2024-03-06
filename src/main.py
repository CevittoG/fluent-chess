import pygame
from pygame.locals import FULLSCREEN, RESIZABLE
from src import Board
from src.visualization import draw_board, draw_pieces, highlight_square, render_players_info
from src.visualization import BOARD_PX_SIZE, SQUARE_PX_SIZE, POSSIBLE_MOVES_COLOR, POSSIBLE_CAPTURES_COLOR, FONT_TYPE, FONT_SIZE, BOARD_MARGIN, BACKGROUND_COLOR
from src.utils import cute_print


def main():
    SEL_PIECE = None  # Stores the currently selected piece (None if no piece is selected)
    SEL_PIECE_ROW = None  # Row index of the selected piece (None if no piece is selected)
    SEL_PIECE_COL = None  # Column index of the selected piece (None if no piece is selected)
    mouse_is_down = False  # Flag to track mouse button state (pressed or released)

    # Initialize Pygame
    cute_print('Game started', 'rocket')
    pygame.init()

    # Set screen size and caption
    screen = pygame.display.set_mode((BOARD_PX_SIZE*2, BOARD_PX_SIZE + SQUARE_PX_SIZE), RESIZABLE)
    pygame.display.set_caption("Chess Sage")
    game_font = pygame.font.Font(FONT_TYPE, FONT_SIZE)

    # Create a game board object
    chessboard = Board()

    # (Optional) Initialize other game elements (e.g., AI, player information)

    # Main game loop
    running = True
    valid_moves = []
    while running:
        # Handle user input (e.g., mouse clicks for move selection)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_is_down = True
                # Check if a piece is clicked within the board area
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row = (mouse_y - BOARD_MARGIN) // SQUARE_PX_SIZE
                col = (mouse_x - BOARD_MARGIN) // SQUARE_PX_SIZE

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
                    new_row = (mouse_y - BOARD_MARGIN) // SQUARE_PX_SIZE
                    new_col = (mouse_x - BOARD_MARGIN) // SQUARE_PX_SIZE

                    # Handle piece movement
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        # Move piece on board and update states
                        chessboard.move_piece(SEL_PIECE, (SEL_PIECE_ROW, SEL_PIECE_COL), (new_row, new_col), valid_moves)

                    # Reset selected piece information
                    SEL_PIECE = None
                    SEL_PIECE_ROW = None
                    SEL_PIECE_COL = None
                    valid_moves = []

        # (Optional) Perform AI move calculation (if applicable)

        # Render the game state (board, pieces, etc.)
        screen.fill(BACKGROUND_COLOR)  # Set background color
        # Prepare light and dark squares
        draw_board(screen)
        # Render players info
        render_players_info(screen, game_font, chessboard)
        # Prepare posible moves
        highlight_square(screen, [position for position, label in valid_moves if 'empty' in label], POSSIBLE_MOVES_COLOR)
        highlight_square(screen, [position for position, label in valid_moves if 'opponent' in label], POSSIBLE_CAPTURES_COLOR)
        # Prepare every piece in the board
        draw_pieces(screen, chessboard, SEL_PIECE_ROW, SEL_PIECE_COL)

        # Update the display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()

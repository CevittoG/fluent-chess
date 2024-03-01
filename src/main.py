import pygame
from src import Piece, Board
from src.visualization import draw_board, draw_pieces, PIECES_IMAGES, BOARD_PX_SIZE, SQUARE_PX_SIZE
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
    screen = pygame.display.set_mode((BOARD_PX_SIZE, BOARD_PX_SIZE))
    pygame.display.set_caption("Chess Sage")

    # Create a game board object
    game_board = Board()

    # (Optional) Initialize other game elements (e.g., AI, player information)

    # Main game loop
    running = True
    while running:
        # Handle user input (e.g., mouse clicks for move selection)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_is_down = True
                # Check if a piece is clicked within the board area
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row = int(mouse_y // SQUARE_PX_SIZE)
                col = int(mouse_x // SQUARE_PX_SIZE)

                if 0 <= row < 8 and 0 <= col < 8:
                    SEL_PIECE = game_board.get_piece_at((row, col))
                    SEL_PIECE_ROW = row
                    SEL_PIECE_COL = col
                    # SEL_PIECE.current_square = SEL_PIECE_ROW, SEL_PIECE_COL
                    # game_board.update_board((SEL_PIECE_ROW, SEL_PIECE_COL), SEL_PIECE)
                    # cute_print(f"{SEL_PIECE.color}_{SEL_PIECE.type}: {SEL_PIECE.current_square}", f'{SEL_PIECE.color}_{SEL_PIECE.type}')

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_is_down = False
                # Check if a piece is released on a valid square
                if SEL_PIECE is not None:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    new_row = int(mouse_y // SQUARE_PX_SIZE)
                    new_col = int(mouse_x // SQUARE_PX_SIZE)

                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        # (Optional) Implement logic to handle piece movement (currently not validated)
                        game_board.move_piece((SEL_PIECE_ROW, SEL_PIECE_COL), (new_row, new_col))
                        cute_print(f"{SEL_PIECE.color}_{SEL_PIECE.type}: ({SEL_PIECE_ROW}, {SEL_PIECE_COL}) -> ({new_row}, {new_col})", f'{SEL_PIECE.color}_{SEL_PIECE.type}')

                    # Reset selected piece information
                    SEL_PIECE = None
                    SEL_PIECE_ROW = None
                    SEL_PIECE_COL = None

        # (Optional) Perform AI move calculation (if applicable)

        # Update and render the game state (board, pieces, etc.)
        screen.fill((255, 255, 255))  # Set background color
        draw_board(screen, game_board)
        draw_pieces(screen, game_board, PIECES_IMAGES, SEL_PIECE_ROW, SEL_PIECE_COL)

        # Update the display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()

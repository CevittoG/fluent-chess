import pygame
from src import Piece, Board
from src.visualization import draw_board, draw_pieces, PIECES_IMAGES, BOARD_SIZE


def main():
    # Initialize Pygame
    pygame.init()

    # Set screen size and caption
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
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

        # (Optional) Perform AI move calculation (if applicable)

        # Update and render the game state (board, pieces, etc.)
        screen.fill((255, 255, 255))  # Set background color
        draw_board(screen, game_board)
        draw_pieces(screen, game_board, PIECES_IMAGES)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()

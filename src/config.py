import pathlib
import pygame


def update_game_dimensions(screen_width):
    # Board Measurements
    BOARD_PX_SIZE = screen_width // 2
    SQUARE_PX_SIZE = BOARD_PX_SIZE // 8
    MARGIN_PX_SIZE = SQUARE_PX_SIZE // 2
    # Font Measurements
    FONT_PX_SIZE_L = MARGIN_PX_SIZE // 2
    FONT_PX_SIZE_M = MARGIN_PX_SIZE // 3
    FONT_PX_SIZE_S = MARGIN_PX_SIZE // 4

    return BOARD_PX_SIZE, SQUARE_PX_SIZE, MARGIN_PX_SIZE, FONT_PX_SIZE_L, FONT_PX_SIZE_M, FONT_PX_SIZE_S


ASPECT_RATIO = 16 / 9

# Directories
MEDIA_DIRECTORY = pathlib.Path(__file__).absolute().parent.parent / 'media'
FONT_DIRECTORY = MEDIA_DIRECTORY / 'fonts'
ICON_DIRECTORY = MEDIA_DIRECTORY / 'icons'

# Image settings
IMG_DIRECTORY = MEDIA_DIRECTORY / 'images'
PIECES_NAMES = ('king', 'queen', 'bishop', 'knight', 'rook', 'pawn')
PIECES_COLORS = ('white', 'black')
PIECES_IMAGES = {f"{color}_{name}": pygame.image.load(str(IMG_DIRECTORY / f"{color}_{name}.png")) for color in PIECES_COLORS for name in PIECES_NAMES}
PIECE_PX_SIZE = list(PIECES_IMAGES.values())[0].get_size()

# Icon Settings
ICON_NAMES = ('king', 'queen', 'bishop', 'knight', 'rook', 'pawn', 'castling', 'promotion', 'sword', 'chess-clock')
ICONS = {f"{name}": pygame.image.load(str(ICON_DIRECTORY / f"{name}.png")) for name in ICON_NAMES}
ICON_PX_SIZE = list(ICONS.values())[0].get_size()

# Font settings
FONT_TTF_FILENAME = 'consola'  # 'micross' 'DMSans-Regular' 'verdana' 'Ubuntu-Regular'
FONT_TYPE = str(FONT_DIRECTORY / f'{FONT_TTF_FILENAME}.ttf')

# Colors
FONT_COLOR = (255, 255, 255)  # (242, 242, 242)
BACKGROUND_COLOR = (40, 40, 40)  # (58, 58, 58)
BOARD_LIGHT_COLOR = (247, 243, 235)
BOARD_DARK_COLOR = (158, 122, 91)
HIGHLIGHT_COLOR = (255, 215, 0)
POSSIBLE_MOVES_COLOR = (102, 187, 106)  # (153, 204, 0) or (139, 172, 139)
POSSIBLE_CAPTURES_COLOR = (204, 0, 0)

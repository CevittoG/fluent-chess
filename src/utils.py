import time
from typing import Union, Tuple


# --------------------------------------------------------------------------------------------------- TERMINAL CUSTOMIZATION
CUTE_PRINT_TABS_LEVEL = 0


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)

        elapsed_time = time.time() - start_time
        if elapsed_time > 60:
            elapsed_time_text = str(round(elapsed_time/60, 2)) + ' min'
        else:
            elapsed_time_text = str(round(elapsed_time, 2)) + ' sec'

        cute_print(f"'{func.__name__}' took {elapsed_time_text}", 'clock')
        return result
    return wrapper


class ColorText:
    RESET = '\033[0m'
    COLORS = {
        'red': '\033[31m',      # errors or important warnings.
        'green': '\033[32m',    # success or completion of a task.
        'yellow': '\033[33m',   # caution or warning.
        'blue': '\033[34m',     # informational message.
        'magenta': '\033[35m',  # highlight important information or to make the text stand out.
        'cyan': '\033[36m',     # highlight important information or to make the text stand out.
        'grey': '\033[37m',     # not important information.
    }

    def __init__(self, text, color='reset'):
        self.text = str(text)
        self.color = color.lower()  # Convert to lowercase for case-insensitivity

    def __str__(self):
        return f'{self.COLORS.get(self.color, self.RESET)}{self.text}{self.RESET}'


class Emoji:
    EMOJIS = {
        'empty': '',
        'bullet': '•',
        'success': '\u2714',            # ✅ Green check mark
        'warning': '\u26a0\ufe0f',      # ⚠️ Warning sign
        'error': '\u274c\ufe0f',        # ❌ Red cross mark
        'star': '\u2B50',               # ⭐ Star
        'info': '\u2139\ufe0f',         # ℹ️ Information
        'arrow_right': '\u2192\ufe0f',  # ➡️ Right arrow
        'download': '\U0001F4E5',       # 📥️ Download Emoji
        'upload': '\U0001F4E4',         # 📤 Upload Emoji
        'next_track': '\u23ed',         # ⏭️ Next Track Button
        'last_track': '\u23ee',         # ⏮️ Last Track Button
        'rocket': '\U0001F680',         # 🚀 Right arrow
        'work': '\u2692\ufe0f',         # 🛠️ Hammer and Wrench
        'finish_flag': '\U0001F3C1',    # 🏁️ Checkered Flag
        'clock': '\U0001F551',          # 🕐 Clock
        'broom': '\U0001F9F9',          # 🧹 Broom
        'mouse': '\U0001f5b1\ufe0f',    # 🖱️ Computer Mouse
        'swords': '\u2694\uFE0F',       # ⚔️ Crossed Swords
        'write': '\U0001F4DD',          # 📝 Memo
        'black_pawn': '\u265F',
        'black_rook': '\u265C',
        'black_knight': '\u265E',
        'black_bishop': '\u265D',
        'black_king': '\u265A',
        'black_queen': '\u265B',
        'white_checker': '\u25FC',
        'white_pawn': '\u2659',
        'white_rook': '\u2656',
        'white_knight': '\u2658',
        'white_bishop': '\u2657',
        'white_king': '\u2654',
        'white_queen': '\u2655',
        'snake': '\U0001F40D'           # 🐍 Snake
    }

    def __init__(self, emoji='empty'):
        self.emoji = emoji.lower()

    def __str__(self):
        return f'{self.EMOJIS.get(self.emoji, self.EMOJIS["empty"])} '


def set_cute_print_tabs(tabs):
    global CUTE_PRINT_TABS_LEVEL
    CUTE_PRINT_TABS_LEVEL = tabs


def cute_print(text: str, emoji_type: str = 'empty', color: str = 'grey'):
    full_text = '\t' * CUTE_PRINT_TABS_LEVEL
    full_text += str(Emoji(emoji_type))
    full_text += text
    full_text = ColorText(full_text, color)
    print(full_text)


def progress_bar(current_iter: int, max_iter: int, start_time: Union[int, float], title: str = None, bar_len: int = 50) -> None:
    """
    Print a progress bar in terminal to follow iterations easily.
    Red (31) is often used to indicate errors or important warnings.
    Green (32) is commonly used to indicate success or completion of a task.
    Yellow (33) is often used to indicate a caution or warning.
    Blue (34) is frequently used to indicate an informational message.
    Magenta (35) and cyan (36) are used to highlight important information or to make the text stand out.
    White (37) is te color normally use.

    :param current_iter: Current iteration number
    :param max_iter: Maximum iteration number
    :param start_time: Time of the first iteration
    :param title: Process title
    :param bar_len: How long the bar should be (optional)
    :return:
    """
    if current_iter > max_iter*0.1:
        color_state = '32'
    elif current_iter > max_iter*0.75:
        color_state = '34'
    else:
        color_state = '37'

    time_spend = time.time() - start_time
    time_estimated = max_iter * time_spend / current_iter
    time_remaining = time_estimated - time_spend

    if time_spend > 3600:
        time_spend_text = f"{round(time_spend / 3600, 2)} hr"
    elif time_spend > 60:
        time_spend_text = f"{round(time_spend / 60, 2)} min"
    else:
        time_spend_text = f"{round(time_spend, 2)} sec"

    if time_estimated > 3600:
        time_estimated_text = f"{round(time_estimated / 3600, 2)} hr"
    elif time_estimated > 60:
        time_estimated_text = f"{round(time_estimated / 60, 2)} min"
    else:
        time_estimated_text = f"{round(time_estimated, 2)} sec"

    if time_remaining > 3600:
        time_remaining_text = f"{round(time_remaining / 3600, 2)} hr"
    elif time_remaining > 60:
        time_remaining_text = f"{round(time_remaining / 60, 2)} min"
    else:
        time_remaining_text = f"{round(time_remaining, 2)} sec"

    bar = f"|{'#' * int(bar_len * (current_iter / max_iter)):{bar_len}s}|"
    progress = f"{current_iter}/{max_iter}"
    percentage = f"{int(100 * (current_iter / max_iter))}%"
    time_count = f"SPENT: {time_spend_text}\t\tREMAINING:{time_remaining_text}\t\tESTIMATED:{time_estimated_text}"

    print(f"\r\033[{color_state}m{title} {bar}\t\t{progress}\t\t{percentage}\t\t|\t\t{time_count}\033[0m", end='')

    if current_iter == max_iter:
        print("")


# --------------------------------------------------------------------------------------------------- POSITIONS (TUPLES)
def adjacent_positions(pos1: tuple, pos2: tuple) -> bool:
    row1, col1 = pos1
    row2, col2 = pos2

    row_distance = abs(row1 - row2)
    col_distance = abs(col1 - col2)

    return row_distance in (-1, 0, 1) and col_distance in (-1, 0, 1)


def find_position(moves: list[tuple[tuple[int, int], str]], position: tuple[int, int]) -> Union[tuple[bool, bool], tuple[tuple, str]]:
    result = False, False
    for move, label in moves:
        if move == position:
            result = (move, label)
            break  # Stop searching once found

    return result


def move_to_chess_notation(piece, start_position: tuple[int, int], end_position: tuple[int, int], capture: Union[bool, str], special_move: Union[bool, dict]) -> str:
    """
    Converts move data into algebraic chess notation.

    Args:
      piece: The piece involved in the move (e.g., 'P', 'N', 'R', 'B', 'Q', 'K').
      start_position: A tuple representing the starting square (row, col).
      end_position: A tuple representing the ending square (row, col).
      capture: Boolean indicating if the move captures a piece (True) or not (False).
      special_move: code from game logging (e.g., queenside_castling, kingside_castling, queen_promotion, bishop_promotion, knight_promotion, rook_promotion)

    Returns:
      The algebraic notation string representing the move.
    """
    piece_notation = {'King': 'K', 'Queen': 'Q', 'Bishop': 'B', 'Knight': 'N', 'Rook': 'R', 'Pawn': 'P'}
    piece = piece_notation[piece]

    notation = ""

    # Include piece name except for pawns and disambiguate if needed
    if piece not in ('P', 'K'):
        notation += piece

    # Disambiguate based on starting file if necessary (multiple pieces can move to the same square)
    if piece in ('R', 'N', 'B') and need_disambiguate(piece, start_position, end_position):
        notation += chr(ord('A') + start_position[1])

    # Add capture symbol if capturing a piece
    if capture:
        notation += "x"

    # Add end position (file and rank)
    notation += position_to_chess_notation(end_position)

    if isinstance(special_move, dict):
        # Add promotion symbol and piece type if promotion occurs
        if special_move['Type'] == 'Promotion':
            notation += "=" + piece_notation[special_move['Obs']]
        # Handle castling moves
        elif special_move['Type'] == 'Castling':
            notation = "O-O" if special_move['Obs'] == 'Kingside' else "O-O-O"  # Kingside or Queenside castling

    return notation


def need_disambiguate(piece, start_position, end_position):
    """
    Checks if a piece move needs disambiguation based on starting and ending positions.

    Args:
        piece: The piece involved in the move (e.g., 'N', 'R', 'B').
        start_position: A tuple representing the starting square (row, col).
        end_position: A tuple representing the ending square (row, col).

    Returns:
        True if disambiguation is needed, False otherwise.
    """

    # Get pieces of the same type on the board (excluding the moving piece)
    # Replace this logic with your actual board state representation to identify potential conflicts
    other_pieces = []  # Replace with logic to find other pieces of the same type
    conflicts = any(piece_position != start_position and move_to_chess_notation(piece, piece_position, end_position, False, False) == move_to_chess_notation(piece, start_position, end_position, False, False) for piece_position in other_pieces)

    return conflicts and piece in ('R', 'N', 'B')


def position_to_chess_notation(position: tuple[int, int]) -> str:
    row, col = position
    # Invert the row and column values to match chess notation (rank, file)
    rank = 8 - row  # Rank starts from 8 and goes down to 1
    file = chr(ord('A') + col)  # Convert column index to uppercase letter

    return f"{file}{rank}"


def seconds_to_hms(seconds: float, milliseconds: bool = False) -> str:
    """Converts a floating-point number of seconds into a string formatted as HH:MM:SS.
        Args:
        seconds: The number of seconds to convert (float).

        Returns:
        A string representing the time in HH:MM:SS format.
    """
    milliseconds = int((seconds % 1) * 1000) if milliseconds else False
    seconds = int(seconds)  # Convert to whole seconds

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)

    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:02d}" if milliseconds else f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return time_str

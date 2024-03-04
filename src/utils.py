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
        'white_queen': '\u2655'
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


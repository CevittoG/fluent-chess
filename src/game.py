import time
from src.utils import cute_print, seconds_to_hms
from src.board import Board
from src.pieces import Piece
from typing import Union, Tuple


class Player:
    def __init__(self, color: str, name: Union[str, None]):
        self.name = name
        self.color = color
        self.time = 0
        self.cumulative_time = 0

    def __str__(self):
        if self.name is None or self.name == '':
            return self.color.title()
        else:
            return self.name


class GameState:
    def __init__(self, chessboard: Board):
        # Timer
        self.start_time = None
        self.time = None
        self.turn_change_mark = None
        self.turn_time = None
        # Game state
        self.state = 'waiting'
        # Logging
        self.log = []
        self.turn_nm = 1
        # Board state
        self.chessboard = chessboard
        # Players state
        self.black_player = None
        self.white_player = None
        self.current_player = None

    def setup_players(self, white_player_name: Union[str, None], black_player_name: Union[str, None]):
        # Create players
        self.white_player = Player('white', white_player_name)
        self.black_player = Player('black', black_player_name)
        # Set white player as first player
        self.current_player = self.white_player

    def start(self, white_player_name: Union[str, None], black_player_name: Union[str, None]):
        self.state = 'running'
        # Timer
        self.start_time = time.time()
        self.time = 0
        self.turn_change_mark = time.time()
        self.turn_time = 0
        # Create players
        self.setup_players(white_player_name, black_player_name)

    def pause(self):
        self.state = 'paused'

    def resume(self):
        self.state = 'running'

    def stop(self):
        self.state = 'stopped'

    def turn(self, start_position: Tuple[int, int], end_position: Tuple[int, int], piece_valid_moves: list[tuple[tuple[int, int], str]]):
        piece = self.chessboard.get_piece_at(start_position)
        # Check if piece about to move is current_player's piece
        if piece.color == self.current_player.color:
            # Make move in board
            move_records = self.chessboard.move_piece(start_position, end_position, piece_valid_moves)
            # Check if movement was valid
            if move_records:
                # Register movement
                self.record_turn(*move_records)
                # Update turn
                self.next_player()
        else:
            cute_print(f"Can't move {piece}, because is {self.current_player}'s turn", f'{piece}', 'yellow')

    def record_turn(self, piece: Piece, s_position: tuple, e_position: tuple, special: Union[bool, dict] = False, capture: Union[bool, str] = False):
        record = {'TurnNumber': self.turn_nm,
                  'Player': {'Name': self.current_player.name,
                             'Color': self.current_player.color.title(),
                             'Time': seconds_to_hms(self.current_player.time, milliseconds=True)},
                  'Move': {'Piece': piece.type.title(),
                           'StartPosition': s_position,
                           'EndPosition': e_position,
                           'Special': special,
                           'Captured': capture,
                           'Time': seconds_to_hms(self.turn_time, milliseconds=True)},
                  'AI': {}}
        self.log.append(record)
        cute_print(f"{record}", 'write')

    def next_player(self):
        self.current_player.cumulative_time += self.turn_time
        self.turn_change_mark = time.time()
        self.current_player = self.black_player if self.current_player.color == 'white' else self.white_player
        self.turn_nm += 1

    def update_elapsed_time(self):
        # Full time since game started (it updates on every main loop of game)
        self.time = time.time() - self.start_time
        self.turn_time = time.time() - self.turn_change_mark
        self.current_player.time = self.current_player.cumulative_time + self.turn_time

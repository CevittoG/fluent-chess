import time
from src.utils import cute_print
from src.board import Board
from src.pieces import Piece
from typing import Union, Tuple, List, Any


class Player:
    def __init__(self, color: str, name: Union[str, None]):
        self.name = name
        self.color = color

    def __str__(self):
        if self.name is None or self.name == '':
            return self.color.title()
        else:
            return self.name


class GameState:
    def __init__(self, chessboard: Board, white_player_name: Union[str, None], black_player_name: Union[str, None]):
        self.state = 'running'
        self.chessboard = chessboard
        self.black_player = None
        self.white_player = None
        self.current_player = None
        self.setup_players(white_player_name, black_player_name)

        self.game_timer = time.time()
        self.log = []
        self.turn_nm = 1

    def setup_players(self, white_player_name: Union[str, None], black_player_name: Union[str, None]):
        # Create players
        self.white_player = Player('white', white_player_name)
        self.black_player = Player('black', black_player_name)
        # Set white player as first player
        self.current_player = self.white_player

    def stop(self):
        self.state = 'stoped'

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
                  'PlayerName': self.current_player.name,
                  'PlayerColor': self.current_player.color.title(),
                  'Move': {'Piece': piece.type.title(),
                           'StartPosition': s_position,
                           'EndPosition': e_position,
                           'Special': special,
                           'Captured': capture},
                  'AI': {}}
        self.log.append(record)
        cute_print(f"{record}", 'write')

    def next_player(self):
        self.turn_nm += 1
        self.current_player = self.black_player if self.current_player.color == 'white' else self.white_player

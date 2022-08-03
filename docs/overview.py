from dataclasses import dataclass
from datetime import datetime


@dataclass
class FileHandler:
    username: str
    dir: str
    paths: str


@dataclass
class RunHandler:
    file_handler: FileHandler


@dataclass
class InputHandler:
    username: str = input()
    edepth: int = input()
    start_date: datetime = input()


@dataclass
class User:
    input_handler: InputHandler  # username, engine depth and startdate
    file_handler: FileHandler  # filepaths
    run_handler: RunHandler  # engine and logger


@dataclass
class Game:
    input_handler: InputHandler  # username, engine depth and startdate
    file_handler: FileHandler  # filepaths
    run_handler: RunHandler  # engine and logger
    iter_metadata: dict  # game_num and tot_games


@dataclass
class Headers:
    input_handler: InputHandler  # username, engine depth and startdate
    file_handler: FileHandler  # filepaths
    run_handler: RunHandler  # engine and logger
    iter_metadata: dict  # game_num, tot_games
    game_metadata: dict  # headers, game_dt, board, game_lists_dict, chess_game


@dataclass
class Move:
    input_handler: InputHandler  # username, engine depth and startdate
    file_handler: FileHandler  # filepaths
    run_handler: RunHandler  # engine and logger
    iter_metadata: dict  # game_num, tot_games,
    game_metadata: dict  # headers, game_dt, board, game_lists_dict, chess_game


@dataclass
class Extract:
    pass


@dataclass
class Export:
    pass


@dataclass
class DataBaseManager:
    pass


@dataclass
class SQLQuerys:
    pass


@dataclass
class Progress:
    pass

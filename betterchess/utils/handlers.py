import logging
import os
from dataclasses import dataclass
from datetime import datetime
from logging import Logger

import chess
import chess.engine
from dotenv import load_dotenv


@dataclass
class InputHandler:
    """Creates and stores user inputs"""

    def collect_user_inputs(self):
        self.username = input("Please enter your username: ")
        self.edepth = int(input("Please enter the engine depth: "))
        self.start_year = input("Please enter the starting year: ")
        self.start_month = input("Please enter the starting month: ")
        self.start_date = datetime(int(self.start_year), int(self.start_month), 1)

    def user_input_dict(self) -> dict:
        """Generates a dictionary object of the users inputs.

        Returns:
            user_inputs (dict): dictionary of user inputs
        """
        user_inputs = {
            "username": self.username,
            "edepth": self.edepth,
            "start_date": self.start_date,
        }
        return user_inputs


@dataclass
class FileHandler:
    """Stores absolute and relative filepaths"""

    username: str
    dir: str = os.path.dirname(__file__)

    # Relative paths
    rpath_stockfish: str = "../../lib/stkfsh_15/stk_15.exe"
    rpath_database: str = "../../data/betterchess.db"
    rpath_temp: str = "../../data/temp.pgn"
    rpath_config_path: str = "../../config/datasets.yaml"

    # Absolute paths
    path_stockfish: str = os.path.join(dir, rpath_stockfish)
    path_database: str = os.path.join(dir, rpath_database)
    path_temp: str = os.path.join(dir, rpath_temp)
    config_path: str = os.path.join(dir, rpath_config_path)

    def __post_init__(self):
        self.rpath_userlogfile: str = f"../../logs/{self.username}.log"
        self.path_userlogfile: str = os.path.join(self.dir, self.rpath_userlogfile)


@dataclass
class RunHandler:
    """_summary_"""

    file_handler: FileHandler

    def create_logger(self) -> Logger:
        """Initializes the Logger object

        Returns:
            Logger: logger object directed at userlogfile path.
        """
        logging.basicConfig(
            filename=self.file_handler.path_userlogfile,
            format="[%(levelname)s %(module)s] %(message)s",
            level=logging.INFO,
            datefmt="%Y/%m/%d %I:%M:%S",
        )
        self.logger = logging.getLogger(__name__)
        return self.logger

    def create_engine(self) -> chess.engine.SimpleEngine:
        """Initializes the chess engine.

        Returns:
            chess.engine.SimpleEngine: Chess engine to enable analysis of games.
        """
        self.engine = chess.engine.SimpleEngine.popen_uci(
            self.file_handler.path_stockfish
        )
        return self.engine


class EnvHandler:
    def __init__(self) -> None:
        self.env_variables = self.create_environment()

    def create_environment(self):
        load_dotenv()
        self.db_type = os.getenv("DB_TYPE")
        return self.db_type

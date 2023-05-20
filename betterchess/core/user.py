"""_summary_
"""
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from logging import Logger
from typing import Tuple

import chess.pgn
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

from betterchess.core.game import Game
from betterchess.utils.extract import Extract
from betterchess.utils.handlers import EnvHandler, FileHandler, InputHandler, RunHandler


@dataclass
class User:
    """Sets up and runs the analysis for all games for a specified user."""

    input_handler: InputHandler
    file_handler: FileHandler
    run_handler: RunHandler
    env_handler: EnvHandler

    def analyse(self) -> None:
        """Extracts users data and runs the analysis on their games."""
        extract = Extract(
            self.input_handler, self.file_handler, self.run_handler, self.env_handler
        )
        extract.run_data_extract(
            self.input_handler.username,
            self.file_handler.path_userlogfile,
            self.run_handler.logger,
        )
        self.run_analysis()

    def run_analysis(self) -> None:
        """Analyses all of the given users games."""
        prepare_users = PrepareUsers()
        all_games, tot_games = prepare_users.current_run(
            self.file_handler.path_database,
            self.input_handler.username,
            self.file_handler.path_userlogfile,
            self.run_handler.logger,
            self.env_handler,
        )
        cleandown = Cleandown()
        cleandown.previous_run(
            self.file_handler.path_userlogfile,
            self.file_handler.path_database,
            self.input_handler.username,
            self.env_handler,
        )
        print("Analysing users data: ")
        for game_num, chess_game in enumerate(all_games["game_data"]):
            preppare_users = PrepareUsers()
            preppare_users.current_game(self.file_handler.path_temp, chess_game)
            iter_metadata = {"game_num": game_num, "tot_games": tot_games}
            game = Game(
                self.input_handler,
                self.file_handler,
                self.run_handler,
                self.env_handler,
                iter_metadata,
            )
            game.run_game_analysis()
            del game


@dataclass
class PrepareUsers:
    """Prepares the current run for analysis e.g. initalises logs, database"""

    def current_run(
        self,
        path_database: str,
        username: str,
        path_userlogfile: str,
        logger: Logger,
        env_handler: EnvHandler,
    ) -> Tuple[pd.DataFrame, int]:
        """_summary_

        Args:
            path_database (str): _description_
            username (str): _description_
            path_userlogfile (str): _description_
            logger (Logger): _description_

        Returns:
            Tuple[pd.DataFrame, int]: _description_
        """
        all_games, tot_games = self.initialise_users_games(
            path_database, username, env_handler
        )
        self.init_game_logs(username, path_userlogfile, logger)
        return (all_games, tot_games)

    def initialise_users_games(
        self, path_database: str, username: str, env_handler: EnvHandler
    ) -> Tuple[pd.DataFrame, int]:
        """Initialise a users games, connects to specified database type and return
        all their games.


        Args:
            path_database (str): Database file path.
            username (str): Username of current run.

        Returns:
            Tuple[pd.DataFrame, int]: all games and the total number of games played
        """
        if env_handler.db_type == "mysql":
            sql_query = """select game_data from pgn_data where username =%s"""
            conn = mysql.connector.connect(
                host=env_handler.mysql_host,
                user=env_handler.mysql_user,
                database=env_handler.mysql_db,
                password=env_handler.mysql_password,
            )
            mysql_engine = create_engine(
                f"{env_handler.mysql_driver}://{env_handler.mysql_user}:{env_handler.mysql_password}@{env_handler.mysql_host}/{env_handler.mysql_db}"
            )
            all_games = pd.read_sql(sql=sql_query, con=mysql_engine, params=[username])
            tot_games = len(all_games["game_data"])
            conn.close()
            return all_games, tot_games
        elif env_handler.db_type == "sqlite":
            sql_query = """select game_data from pgn_data where username =:username"""
            params = {"username": username}
            conn = sqlite3.connect(path_database)
            all_games = pd.read_sql(sql=sql_query, con=conn, params=params)
            tot_games = len(all_games["game_data"])
            conn.close()
            return all_games, tot_games

    def init_game_logs(
        self, username: str, path_userlogfile: str, logger: Logger
    ) -> None:
        """Initialises the log file and sets the first games log date.

        Args:
            username (str): Username of current run.
            path_userlogfile (str): Logfile for the current user.
            logger (Logger): Logger object.
        """
        if self.numlines_in_logfile(path_userlogfile) == 0:
            self.set_first_game_logdate(username, path_userlogfile, logger)

    def numlines_in_logfile(self, path_userlogfile: str) -> int:
        """Returns the number of lines in the logfile.

        Args:
            path_userlogfile (str): Logfile for the current user.

        Returns:
            int: Number of games in logfile.
        """
        game_log_list = []
        with open(path_userlogfile, "r") as log_file:
            lines = log_file.readlines()
            self.check_logfile(game_log_list, lines)
        return len(game_log_list)

    def set_first_game_logdate(
        self, username: str, path_userlogfile: str, logger: Logger
    ) -> None:
        """Creates the default date in the logfile.

        Args:
            username (str): Username of current run.
            path_userlogfile (str): Logfile for the current user.
            logger (Logger): Logger object.
        """
        with open(path_userlogfile, mode="a") as _:
            game_num = 0
            init_dt = datetime(2020, 1, 1)
            logger.info(f"| {username} | {init_dt} | {game_num}")

    def check_logfile(self, game_log_list: list, lines: list[str]) -> None:
        """Appends a given logged line to `game_log_list` if it is part of the module
        "user" or "user_analysis"

        Args:
            game_log_list (list): List of logged games in logfile
            lines (list[str]): Lines in the logfile
        """
        game_log_list.extend(
            line for line in lines if ("user" in line) or ("user_analysis" in line)
        )

    def current_game(self, path_temp: str, chess_game: chess.pgn.Game) -> None:
        """Writes the current game to temp.pgn.

        Args:
            path_temp (str): path to temp.pgn file
            chess_game (chess.pgn.Game): chess game for analysis
        """
        with open(path_temp, mode="w") as temp_file:
            temp_file.write(str(chess_game.replace(" ; ", "\n")))


@dataclass
class Cleandown:
    """Cleans down the previous run e.g. remove unfinished analysis for a game, reset logs."""

    def previous_run(
        self,
        path_userlogfile: str,
        path_database: str,
        username: str,
        env_handler: EnvHandler,
    ) -> None:
        """Runs the cleandown of the previous run

        Args:
            path_userlogfile (str):  Logfile for the current user.
            path_database (str): Database file path.
            username (str): Username of current run.
        """
        game_num = self.get_last_logged_game_num(path_userlogfile)
        self.clean_sql_table(path_database, game_num, username, env_handler)

    def clean_sql_table(
        self, path_database: str, game_num: int, username: str, env_handler: EnvHandler
    ) -> None:
        """_summary_

        Args:
            path_database (str): Database file path.
            game_num (int): Latest unfinished game number of the current user.
            username (str): Username of current run.
        """
        if env_handler.db_type == "mysql":
            conn = mysql.connector.connect(
                host=env_handler.mysql_host,
                user=env_handler.mysql_user,
                database=env_handler.mysql_db,
                password=env_handler.mysql_password,
            )
            curs = conn.cursor()
            curs.execute(
                """DELETE FROM move_data WHERE Game_number = %s and Username = %s""",
                (game_num, username),
            )
            conn.commit()
            curs.close()
        elif env_handler.db_type == "sqlite":
            conn = sqlite3.connect(path_database)
            curs = conn.cursor()
            sql_query = "DELETE FROM move_data WHERE Game_number = :game_num and Username = :username"
            params = {"game_num": game_num, "username": username}
            curs.execute(sql_query, params)
            conn.commit()
            curs.close()

    def get_last_logged_game_num(self, path_userlogfile: str) -> int:
        """Gets the last logged games number.

        Args:
            path_userlogfile (str): path to logfile.

        Returns:
            int: last logged game number.
        """
        if self.logfile_not_empty(path_userlogfile):
            log_list = self.get_game_log_list(path_userlogfile)
            return int(log_list[-1].split("|")[3].strip())

    def logfile_not_empty(self, path_userlogfile: str) -> bool:
        """Checks to see if the logfile is empty.

        Args:
            path_userlogfile (str): path to logfile.

        Returns:
            bool: Whether the log file is empty
        """
        with open(path_userlogfile, mode="r") as log_file:
            lines = log_file.readlines()
        return bool(lines)

    def get_game_log_list(self, path_userlogfile: str) -> list:
        """Returns the number of lines in the logfile = "user" or "analysis".

        Args:
            path_userlogfile (str): path to logfile.

        Returns:
            list: List of logged games.
        """
        game_log_list = []
        with open(path_userlogfile, mode="r") as log_file:
            lines = log_file.readlines()
            self.logfile_line_checker_multi(game_log_list, lines)
        return game_log_list

    def logfile_line_checker_multi(self, game_log_list: list, lines: list[str]) -> None:
        """_summary_

        Args:
            game_log_list (list):  List of logged games.
            lines (list[str]): Lines in the log file.
        """
        game_log_list.extend(
            line for line in lines if ("user" in line) or ("game" in line)
        )

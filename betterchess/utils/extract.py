import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from logging import Logger

import chessdotcom
import mysql.connector
import pandas as pd
import requests
from sqlalchemy import create_engine

from betterchess.utils.handlers import EnvHandler, FileHandler, InputHandler, RunHandler


@dataclass
class Extract:
    """_summary_

    Returns:
        _type_: _description_
    """

    input_handler: InputHandler
    file_handler: FileHandler
    run_handler: RunHandler
    env_handler: EnvHandler

    def run_data_extract(
        self, username: str, path_database: str, path_userlogfile: str, logger: Logger
    ) -> None:
        """_summary_

        Args:
            username (str): _description_
            dbfilepath (str): _description_
            logfilepath (str): _description_
            logger (Logger): _description_
        """
        username_list, url_date_list, games_list = [], [], []
        self.init_user_logfile(username, logger)
        urls = chessdotcom.get_player_game_archives(username).json
        num_urls = len(urls["archives"])
        pgn_df = self.get_data_from_urls(
            urls,
            num_urls,
            logger,
            path_userlogfile,
            username,
            path_database,
            username_list,
            url_date_list,
            games_list,
        )
        self.export_pgn_data(pgn_df)

    def init_user_logfile(self, username: str, logger: Logger) -> None:
        """_summary_

        Args:
            logger (Logger): _description_
            username (str): _description_
        """
        init_extlogger = datetime(2000, 1, 1)
        logger.info(f"| {username} | {init_extlogger}")

    def get_data_from_urls(
        self,
        urls: json,
        num_urls: int,
        logger: Logger,
        path_userlogfile: str,
        username: str,
        path_database: str,
        username_list: list,
        url_date_list: list,
        games_list: list,
    ) -> pd.DataFrame:
        """_summary_

        Args:
            urls (json): _description_
            num_urls (int): _description_
            logger (Logger): _description_
            path_userlogfile (str): _description_
            username (str): _description_
            path_database (str): _description_
            username_list (list): _description_
            url_date_list (list): _description_
            games_list (list): _description_

        Returns:
            pd.DataFrame: _description_
        """
        for url_num, url in enumerate(urls["archives"]):
            self.simple_progress_bar(url_num, num_urls)
            in_curr = self.in_curr_month(url)
            in_log = self.url_in_log(url, path_userlogfile)
            url_date = self.get_url_date(url)
            logger.info(f"| {username} | {url_date}")
            url_games_list = self.extract_filter(
                username=username,
                in_log=in_log,
                in_curr=in_curr,
                url=url,
            )
            try:
                for game in url_games_list:
                    username_list.append(username)
                    url_date_list.append(url_date)
                    games_list.append(game)
            except TypeError:
                continue
        game_dict = {
            "username": username_list,
            "url_date": url_date_list,
            "game_data": games_list,
        }
        pgn_df = pd.DataFrame(game_dict)
        return pgn_df

    def export_pgn_data(self, pgn_df: pd.DataFrame) -> None:
        """_summary_

        Args:
            path_database (str): _description_
            pgn_df (pd.DataFrame): _description_
        """
        conn = mysql.connector.connect(
            host=self.env_handler.mysql_host,
            user=self.env_handler.mysql_user,
            database=self.env_handler.mysql_db,
            password=self.env_handler.mysql_password,
        )
        mysql_engine = create_engine(
            f"{self.env_handler.mysql_driver}://{self.env_handler.mysql_user}:{self.env_handler.mysql_password}@{self.env_handler.mysql_host}/{self.env_handler.mysql_db}"
        )
        pgn_df.to_sql(
            name="pgn_data", con=mysql_engine, if_exists="append", index=False
        )
        conn.commit
        conn.close

    def extract_filter(
        self, username: str, in_log: bool, in_curr: bool, url: str
    ) -> list:
        """_summary_

        Args:
            username (str): _description_
            in_log (bool): _description_
            in_curr (bool): _description_
            url (str): _description_
            path_database (str): _description_

        Returns:
            list: _description_
        """
        empty_list = []
        if not in_log:
            return self.collect_game_data(url)
        elif in_log and not in_curr:
            return empty_list
        elif in_log and in_curr:
            self.filter_pgn_table(username)
            return self.collect_game_data(url)

    def filter_pgn_table(self, username: str) -> None:
        """_summary_

        Args:
            username (str): _description_
            path_database (str): _description_
        """
        curr_month = self.get_curr_mth()
        conn = mysql.connector.connect(
            host=self.env_handler.mysql_host,
            user=self.env_handler.mysql_user,
            database=self.env_handler.mysql_db,
            password=self.env_handler.mysql_password,
        )
        curs = conn.cursor()
        curs.execute(
            """delete from pgn_data where username = %s and url_date = %s""",
            (username, curr_month),
        )
        conn.commit()
        conn.close()

    def collect_game_data(self, url: str) -> list:
        """_summary_

        Args:
            url (str): _description_

        Returns:
            list: _description_
        """
        response = requests.get(url)
        data = response.json()
        url_games_list = []
        for game_pgn in data["games"]:
            chess_game_string = str(game_pgn["pgn"]).replace("\n", " ; ")
            url_games_list.append(chess_game_string)
        return url_games_list

    def url_in_log(self, url: str, path_userlogfile: str) -> bool:
        """_summary_

        Args:
            url (str): _description_
            path_userlogfile (str): _description_

        Returns:
            bool: _description_
        """
        url_date = self.get_url_date(url)
        with open(path_userlogfile, "r") as log_file:
            lines = log_file.readlines()
        url_date_list = []
        for line in lines:
            log_url_date = datetime.strptime(
                line.split("|")[2].strip(), "%Y-%m-%d %H:%M:%S"
            )
            url_date_list.append(log_url_date)
        if url_date in url_date_list:
            return True
        else:
            return False

    def in_curr_month(self, url: str) -> bool:
        """_summary_

        Args:
            url (str): _description_

        Returns:
            bool: _description_
        """
        url_date = self.get_url_date(url)
        curr_mth = self.get_curr_mth()
        if curr_mth == url_date:
            return True
        else:
            return False

    def get_curr_mth(self) -> datetime:
        """_summary_

        Returns:
            datetime: _description_
        """
        yr = datetime.now().year
        mth = datetime.now().month
        day = 1
        curr_mth = datetime(yr, mth, day)
        return curr_mth

    def get_url_date(self, url: str) -> datetime:
        """_summary_

        Args:
            url (str): _description_

        Returns:
            datetime: _description_
        """
        x = url.split("/")[7:]
        yr, mth = x[0], x[1]
        url_date = datetime(int(yr), int(mth), 1)
        return url_date

    def simple_progress_bar(self, num: int, num_urls: int) -> None:
        """_summary_

        Args:
            num (int): _description_
            total (int): _description_
        """
        x = "of User's data extracted"
        percent = 100 * ((num + 1) / float(num_urls))
        bar = "❚" * int(percent / 2.5) + "-" * (40 - int(percent / 2.5))
        print(f"\r| {bar}| {percent:.2f}% {x}", end="\r")

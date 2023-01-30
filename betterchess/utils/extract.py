import json
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
    """Class for extracting the current users game data from chess.com"""

    input_handler: InputHandler
    file_handler: FileHandler
    run_handler: RunHandler
    env_handler: EnvHandler

    def run_data_extract(
        self, username: str, path_userlogfile: str, logger: Logger
    ) -> None:
        """Runs the current data extract.

        Args:
            username (str): Current users username.
            logfilepath (str): Logfile path.
            logger (Logger): Logger object.
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
            username_list,
            url_date_list,
            games_list,
        )
        self.export_pgn_data(pgn_df)

    def init_user_logfile(self, username: str, logger: Logger) -> None:
        """Initalises the current users logfile.

        Args:
            logger (Logger): Logger object.
            username (str): Current users username.
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
        username_list: list,
        url_date_list: list,
        games_list: list,
    ) -> pd.DataFrame:
        """Extracts the filtered user game data and creates a dataframe.

        Args:
            urls (json): All the monthly urls extracted for chess.com for a given user.
            num_urls (int): Number of urls extracted.
            logger (Logger): Logger object.
            path_userlogfile (str): Logfile path.
            username (str): Current users username.
            username_list (list): list of repeated username.
            url_date_list (list): list of repeated url dates.
            games_list (list): list of chess games data.

        Returns:
            pd.DataFrame: pgn game data table.
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
        """Extracts teh pgn game data from a given database type.

        Args:
            pgn_df (pd.DataFrame): pgn data table.
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
        """Filters the data extract to only pull new games.

        Args:
            username (str): Current users username.
            in_log (bool): Is the current months extract in the logfile.
            in_curr (bool): Is the current months extract also the current month.
            url (str): Extract url.

        Returns:
            list: game data.
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
        """Filters the pgn table by removing games which have been extracted allready
        and it is still the same month.

        Args:
            username (str): Current users username.
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
        """Collects the game data from chess.com.

        Args:
            url (str): A given chess.com api url.

        Returns:
            list: list of game data for that url month.
        """
        response = requests.get(url)
        data = response.json()
        url_games_list = []
        for game_pgn in data["games"]:
            chess_game_string = str(game_pgn["pgn"]).replace("\n", " ; ")
            url_games_list.append(chess_game_string)
        return url_games_list

    def url_in_log(self, url: str, path_userlogfile: str) -> bool:
        """Checks if the current url has allready been added to the logfile.

        Args:
            url (str): A given chess.com api url.
            path_userlogfile (str): path_userlogfile (str): Logfile path.

        Returns:
            bool: True if url is in the logfile.
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
        """Checks if the url month date is the current month date.

        Args:
            url (str): A given chess.com api url.

        Returns:
            bool: True if url in the current month.
        """
        url_date = self.get_url_date(url)
        curr_mth = self.get_curr_mth()
        if curr_mth == url_date:
            return True
        else:
            return False

    def get_curr_mth(self) -> datetime:
        """Gets the current month.

        Returns:
            curr_mth (datetime): Current month.
        """
        yr = datetime.now().year
        mth = datetime.now().month
        day = 1
        curr_mth = datetime(yr, mth, day)
        return curr_mth

    def get_url_date(self, url: str) -> datetime:
        """Gets the urls urls date.

        Args:
            url (str): A given chess.com api url.

        Returns:
            datetime: url date.
        """
        x = url.split("/")[7:]
        yr, mth = x[0], x[1]
        url_date = datetime(int(yr), int(mth), 1)
        return url_date

    def simple_progress_bar(self, num: int, num_urls: int) -> None:
        """Simple visual progress bar to track the extract progress.

        Args:
            num (int): Current url being extracted.
            total (int): Total number of urls to be extracted.
        """
        x = "of User's data extracted"
        percent = 100 * ((num + 1) / float(num_urls))
        bar = "❚" * int(percent / 2.5) + "-" * (40 - int(percent / 2.5))
        print(f"\r| {bar}| {percent:.2f}% {x}", end="\r")

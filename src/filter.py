"""
Module for filtering the move_data.csv file to remove any
incomplete games.
"""
import sqlite3
from datetime import datetime
from logging import Logger
from os.path import exists
from pandas import DataFrame

COL_NAMES = [
    "Username",
    "Game_date",
    "edepth",
    "Game_number",
    "Move_number",
    "Move",
    "Move_eval",
    "Best_move",
    "Best_move_eval",
    "Move_eval_diff",
    "Move accuracy",
    "Move_type",
    "Piece",
    "Move_colour",
    "Castling_type",
    "White_castle_num",
    "Black_castle_num",
    "Move_time",
]


def clean_sql_table(database: str, game_num: int, username: str):
    conn = sqlite3.connect(database=database)
    curs = conn.cursor()
    sql_query = (
        "DELETE FROM move_data WHERE Game_number = :game_num and Username = :username"
    )
    params = {"game_num": game_num, "username": username}
    curs.execute(sql_query, params)
    conn.commit()
    curs.close()


def get_last_logged_game_num(logfilepath: str) -> int:
    """Gets the last logged games number.

    Args:
        logfilepath (str): path to logfile.

    Returns:
        int: last logged game number.
    """
    if logfile_not_empty(logfilepath=logfilepath):
        log_list = get_game_log_list(logfilepath=logfilepath)
        last_logged_game_num = int(log_list[-1].split("|")[3].strip())
        return last_logged_game_num
    else:
        pass


def get_last_logged_game(logfilepath: str) -> datetime:
    """Returns the last logged game datatime."""
    game_log_list = get_game_log_list(logfilepath=logfilepath)
    llog = game_log_list[-1]
    llog_date_str = llog.split("|")[2].strip()
    llog_date = datetime.strptime(llog_date_str, "%Y-%m-%d %H:%M:%S")
    return llog_date


def file_exist(movefilepath: str):
    """Checks to see if a file exists."""
    file_exists = exists(path=movefilepath)
    if file_exists:
        pass
    else:
        with open(file=movefilepath, mode="w") as _:
            pass
    return file_exists


def logfile_not_empty(logfilepath: str) -> bool:
    """Checks to see if the logfile is empty."""
    with open(file=logfilepath, mode="r") as log_file:
        lines = log_file.readlines()
    if not (not lines):
        return True
    else:
        return False


def get_game_log_list(logfilepath: str) -> list:
    """Returns the number of lines in the logfile = "filter"."""
    game_log_list = []
    with open(file=logfilepath, mode="r") as log_file:
        lines = log_file.readlines()
        logfile_line_checker_multi(game_log_list=game_log_list, lines=lines)
    return game_log_list


def logfile_line_checker_multi(game_log_list: list, lines: list[str]) -> None:
    for line in lines:
        if "filter" in line:
            game_log_list.append(line)
        elif "user_analysis" in line:
            game_log_list.append(line)


def init_game_logs(username: str, logfilepath: str, logger: Logger) -> None:
    """Initalises the logfile."""
    if numlines_in_logfile(logfilepath=logfilepath) != 0:
        pass
    else:
        set_first_game_logdate(
            username=username, logfilepath=logfilepath, logger=logger
        )


def numlines_in_logfile(logfilepath: str) -> int:
    """Returns the number of lines in the logfile = "filter"."""
    game_log_list = []
    with open(logfilepath, "r") as log_file:
        lines = log_file.readlines()
        logfile_line_checker_multi(game_log_list=game_log_list, lines=lines)
    return len(game_log_list)


def set_first_game_logdate(username: str, logfilepath: str, logger: Logger) -> None:
    """Creates the default date in the logfile."""
    with open(file=logfilepath, mode="a") as _:
        game_num = 0
        init_dt = datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        logger.info(f"| {username} | {init_dt} | {game_num}")


def logfile_line_checker_single(log_list: list, lines: list[str]) -> None:
    for line in lines:
        if "filter" in line:
            log_list.append(line)

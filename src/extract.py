"""Extracts the data of a given chess.com user."""
import logging
import requests
import pandas as pd
from chessdotcom import get_player_game_archives
from datetime import datetime


def data_extract(username: str, filepath: str, logfilepath: str) -> None:
    '''Extracts user data for a given username.
    Args:
        username: specified username input.
        filepath: filepath for csv storage.
        extlogger: extract logger.
    Returns:
        outputs a csv file of the users pgn game data.
    '''
    urls = get_player_game_archives(username).json
    all_games = []
    for url in urls["archives"]:
        extlogger = create_extlogger(logfilepath, "extlogger")
        
        # curr_dtc = is_curr_month(url)
        # # in_log = is_date_in_logfile()
        # extract_filter(curr_dtc, in_log)

        data = requests.get(url).json()
        for game_pgn in data["games"]:
            chess_game_string = str(game_pgn["pgn"])
            all_games.append(chess_game_string)

    game_dict = {"game_data": all_games}
    df = pd.DataFrame(game_dict, columns=["game_data"])
    df.to_csv(filepath, index=False)


def collect_games(urls):
    pass


def extract_filter():
    pass


def is_date_in_logfile(url):
    url_date = get_url_date(url)
    pass


def is_curr_month(url):
    """Checks to see if the extracted month equals the current month"""
    url_date = get_url_date(url)
    curr_mth = get_curr_mth()
    if curr_mth == url_date:
        return True
    else:
        return False


def get_curr_mth():
    cyv = datetime.now().year
    cmv = datetime.now().month
    curr_mth = datetime.strptime(
        f"{cyv}-{cmv}-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    return curr_mth


def get_url_date(url):
    """Returns the date of the url as datatime."""
    x = url.split("/")[7:]
    yr, mth = x[0], x[1]
    url_date = datetime.strptime(
        f"{yr}-{mth}-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    return url_date


def filter_pgn():
    """Removes games of the current month in the csv
     and then reruns the extract for that month."""


def create_extlogger(extfilepath, name):
    logging.basicConfig(
        filename=extfilepath,
        format='[%(levelname)s %(module)s] %(message)s',
        level=logging.INFO, datefmt='%Y/%m/%d %I:%M:%S')
    extlogger = logging.getLogger(name)
    return extlogger


# def rerun_filter():
#     '''Collects the date of most recent game played for a given user'''
#     game_number = 0
#     logging.basicConfig(filename=file_logger,
#                         format='[%(levelname)s %(module)s] %(message)s',
#                         level=logging.INFO, datefmt='%Y/%m/%d %I:%M:%S')
#     logger = logging.getLogger(__name__)
#     # Opens log file
#     with open(file_logger, "r") as log_file:
#         lines = log_file.readlines()
#     # If log file empty set inital date.
#     if not lines:
#         with open(file_logger, "w") as _:
#             init_dt = datetime.strptime("2000-01-01 00:00:00",
#                                         '%Y-%m-%d %H:%M:%S')
#             logger.info(f"Game info | {init_dt} | {game_number}")
#     # gets .
#     else:
#         llog = lines[-1]
#         llog_date_str = llog.split("|")[1].strip()
#         llog_date = datetime.strptime(llog_date_str, '%Y-%m-%d %H:%M:%S')
#         return llog_date


# def clean_rerun_files():
#     '''Removes last unfinished games moves from the move_data csv.'''
#     # Check to see whether move data file exists
#     file_exists = exists(file_move_data)
#     if file_exists:
#         pass
#     else:
#         with open(file_move_data, "w") as _:
#             pass
#     # Opens logging file
#     with open(file_logger, "r") as log_file:
#         lines = log_file.readlines()
#     # Cleans csv file if not empty
#     if not lines:
#         pass
#     else:
#         if file_exists:
#             llog = lines[-1]
#             llog_gn = int(llog.split("|")[2].strip())
#             col_names = ["Username",
#                          "Date",
#                          "Game_number",
#                          "Engine_Depth",
#                          "Game_date",
#                          "Move_number",
#                          "Move",
#                          "Best_move",
#                          "Move_eval",
#                          "Best_move_eval",
#                          "Move_eval_diff",
#                          "Move accuracy",
#                          "Move_type"]
#             unclean_df = pd.read_csv(file_move_data, names=col_names)
#             df_filter = unclean_df["Game_number"] != llog_gn
#             clean_df = unclean_df[df_filter]
#             clean_df.to_csv(file_move_data, mode="w",
#                             index=False, header=False)
#         else:
#             pass
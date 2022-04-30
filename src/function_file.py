import logging
import pandas as pd
import os
from os.path import exists
from datetime import datetime
import parameters


dirn = os.path.dirname(__file__)
file_logger = os.path.join(dirn,
                           rf"../logs/{parameters.username}_game_log.txt")
file_move_data = os.path.join(dirn,
                              r'../data/move_data.csv')


def rerun_filter():
    '''Collects the date of most recent game played for a given user'''
    game_number = 0
    logging.basicConfig(filename=file_logger,
                        format='[%(levelname)s %(module)s] %(message)s',
                        level=logging.INFO, datefmt='%Y/%m/%d %I:%M:%S')
    logger = logging.getLogger(__name__)
    # Opens log file
    with open(file_logger, "r") as log_file:
        lines = log_file.readlines()
    # If log file empty set inital date.
    if not lines:
        with open(file_logger, "w") as _:
            init_dt = datetime.strptime("2000-01-01 00:00:00",
                                        '%Y-%m-%d %H:%M:%S')
            logger.info(f"Game info | {init_dt} | {game_number}")
    # gets .
    else:
        llog = lines[-1]
        llog_date_str = llog.split("|")[1].strip()
        llog_date = datetime.strptime(llog_date_str, '%Y-%m-%d %H:%M:%S')
        return llog_date


def clean_rerun_files():
    '''Removes last unfinished games moves from the move_data csv.'''
    # Check to see whether move data file exists
    file_exists = exists(file_move_data)
    if file_exists:
        pass
    else:
        with open(file_move_data, "w") as _:
            pass
    # Opens logging file
    with open(file_logger, "r") as log_file:
        lines = log_file.readlines()
    # Cleans csv file if not empty
    if not lines:
        pass
    else:
        if file_exists:
            llog = lines[-1]
            llog_gn = int(llog.split("|")[2].strip())
            col_names = ["Username",
                         "Date",
                         "Game_number",
                         "Engine_Depth",
                         "Game_date",
                         "Move_number",
                         "Move",
                         "Best_move",
                         "Move_eval",
                         "Best_move_eval",
                         "Move_eval_diff",
                         "Move accuracy",
                         "Move_type"]
            unclean_df = pd.read_csv(file_move_data, names=col_names)
            df_filter = unclean_df["Game_number"] != llog_gn
            clean_df = unclean_df[df_filter]
            clean_df.to_csv(file_move_data, mode="w",
                            index=False, header=False)
        else:
            pass

from datetime import datetime
import logging
import pandas as pd
from os.path import exists
import os

dirname = os.path.dirname(__file__)
file_logger = os.path.join(dirname, r"../docs/chess_game_logger.txt")
file_move_data = os.path.join(dirname, r'../data/move_data.csv')


def rerun_filter():
    '''
    stuff
    '''
    logging.basicConfig(filename=file_logger, format='[%(levelname)s %(module)s] %(asctime)s - %(message)s', level=logging.INFO, datefmt='%Y/%m/%d %I:%M:%S')
    logger = logging.getLogger(__name__)
    game_number = 0

    with open(file_logger, "r") as log_file:
        lines = log_file.readlines()

    if not lines:
        with open(file_logger, "w") as f:
            init_dt = datetime.strptime("2000-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
            logger.info(f"DateTime of last game entry | {init_dt} | {game_number}")
    else:
        llog = lines[-1]
        llog_date_str = llog.split("|")[1].strip()
        llog_date = datetime.strptime(llog_date_str, '%Y-%m-%d %H:%M:%S')
        return llog_date    


def clean_rerun_files():
    '''
    stuff
    '''
    file_exists = exists(file_move_data)

    if file_exists:
        pass
    else:
        init_file = pd.DataFrame(list())
        init_file.to_csv(file_move_data)

    with open(file_logger, "r") as log_file:
        lines = log_file.readlines()

    if not lines:
        pass
    else:
        if file_exists:
            llog = lines[-1]
            llog_gn = int(int(llog.split("|")[2].strip())+1)
            col_names = ["Date", "Game_number", "Engine_Depth", "Game_date", "Move_number",
                         "Move", "Best_move", "Move_eval", "Best_move_eval", "Move_eval_diff",
                         "Move accuracy", "Move_type"]
            unclean_df = pd.read_csv(file_move_data, names=col_names)
            df_filter = unclean_df["Game_number"] != llog_gn
            clean_df = unclean_df[df_filter]
            clean_df.to_csv(file_move_data, mode="w", index=False, header=False)
        else:
            pass

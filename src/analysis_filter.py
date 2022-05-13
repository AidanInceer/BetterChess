from logging import Logger
from datetime import datetime
import pandas as pd
from os.path import exists


def init_game_logs(logfilepath: str, logger: Logger) -> Logger:
    game_log_list = []
    with open(logfilepath, "r") as log_file:
        lines = log_file.readlines()
        for line in lines:
            if "analysis_filter" in line:
                game_log_list.append(line)
    if len(game_log_list) != 0:
        pass
    else:
        with open(logfilepath, "a") as _:
            game_num = 0
            init_dt = datetime.strptime("2000-01-01 00:00:00",
                                        '%Y-%m-%d %H:%M:%S')
            logger.info(f"| {init_dt} | {game_num}")


def llog_game(logfilepath: str):
    game_log_list = []
    with open(logfilepath, "r") as log_file:
        lines = log_file.readlines()
        for line in lines:
            if "analysis_filter" in line:
                game_log_list.append(line)
            if "user_analysis" in line:
                game_log_list.append(line)
    llog = game_log_list[-1]
    llog_date_str = llog.split("|")[1].strip()
    llog_date = datetime.strptime(llog_date_str, '%Y-%m-%d %H:%M:%S')
    return llog_date


def clean_movecsv(movefilepath: str, logfilepath: str):
    '''Removes last unfinished games moves from the move_data csv.'''
    file_exists = file_exist(movefilepath)
    log_not_empty = is_logfile_empty(logfilepath)
    if log_not_empty and file_exists:
        log_list = []
        with open(logfilepath, "r") as log_file:
            lines = log_file.readlines()
            for line in lines:
                if "analysis_filter" in line:
                    log_list.append(line)
                if "user_analysis" in line:
                    log_list.append(line)
        llog = log_list[-1]
        print(llog)
        llog_gn = int(llog.split("|")[2].strip())
        col_names = [
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
            "Move_type"]
        unclean_df = pd.read_csv(movefilepath, names=col_names)
        df_filter = unclean_df["Game_number"] != llog_gn
        clean_df = unclean_df[df_filter]
        clean_df.to_csv(movefilepath, mode="w",
                        index=False, header=None)
    else:
        pass


def file_exist(movefilepath: str):
    file_exists = exists(movefilepath)
    if file_exists:
        pass
    else:
        with open(movefilepath, "w") as _:
            pass
    return file_exists


def is_logfile_empty(logfilepath: str):
    with open(logfilepath, "r") as log_file:
        lines = log_file.readlines()
    if not lines:
        has_lines = False
    else:
        has_lines = True
    return has_lines

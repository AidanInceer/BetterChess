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
            "Move_type",
            "Piece",
            "Move_colour",
            "Castling_type",
            "White_castle_num",
            "Black_castle_num",
            "Move_time"]
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


# def column_headers(file_g_data, file_m_data):
#     game_header_list = [
#         "Username", "Date", "Game_number", "Engine_depth",
#         "Game_type", "White_player",
#         "Black_player", "White_rating", "Black_rating",
#         "User_colour", "User_rating", "opponent_rating",
#         "User_winner", "Opening_name",
#         "Opening_class", "Termination", "Number_of_moves",
#         "Accuracy", "Opening_accuracy", "Mid_accuracy",
#         "End_accuracy", "No_best", "No_great", "No_good",
#         "No_ok", "No_inaccuracy", "No_mistake",
#         "No_blunder", "Improvement"]

#     move_header_list = [
#         "Username", "Date", "Game_number", "edepth",
#         "Move_number", "Move",
#         "Best_move", "Move_eval", "Best_move_eval",
#         "Move_eval_diff", "Move accuracy", "Move_type"]
#     game_data = pd.read_csv(file_g_data, header=None)
#     game_header_list = game_header_list
#     if "Username" in game_data.iloc[0, 0]:
#         game_data.to_csv(file_g_data, header=False, index=False)
#     else:
#         game_data.to_csv(file_g_data, header=game_header_list, index=False)
#     #   Move data
#     move_data = pd.read_csv(file_m_data, header=None)
#     move_header_list = move_header_list
#     if "Username" in move_data.iloc[0, 0]:
#         move_data.to_csv(file_m_data, header=False, index=False)
#     else:
#         move_data.to_csv(file_m_data, header=move_header_list, index=False)

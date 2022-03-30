import numpy as np
import math
from datetime import datetime
import logging
import pandas as pd
from os.path import exists
import os

dirname = os.path.dirname(__file__)
file_logger = os.path.join(dirname, r"../docs/chess_game_logger.txt")
file_move_data = os.path.join(dirname, r'../data/move_data.csv')

def move_best_eval_calc(get_eval_best_move_init):
    get_eval_best_move = str(get_eval_best_move_init['score'].white())
    if "#" in get_eval_best_move:
        get_eval_best_move = get_eval_best_move[1:]
    else:
        get_eval_best_move = get_eval_best_move
    get_eval_best_move = int(get_eval_best_move)
    return get_eval_best_move


def move_mainline_eval_calc(get_eval_mainline_init):
    get_eval_mainline = str(get_eval_mainline_init['score'].white())
    if "#" in get_eval_mainline:
        get_eval_mainline = get_eval_mainline[1:]
    else:
        get_eval_mainline = get_eval_mainline
    get_eval_mainline = int(get_eval_mainline)
    return get_eval_mainline


def eval_diff(move_num, get_eval_best_move, get_eval_mainline):
    # Calculation of eval diff
    if move_num % 2 == 0:
        # Calculation of move accuracy for white
        move_eval_diff = round(abs(get_eval_best_move - get_eval_mainline), 3)
        return move_eval_diff
    else:
        # Calculation of move accuracy for black
        move_eval_diff = round(abs(get_eval_mainline - get_eval_best_move), 3)
        return move_eval_diff


def move_acc_func(move_eval_diff):
    mean = 0
    variation = 0.75
    move_accuracy = round(math.exp(-0.00005 * ((move_eval_diff - mean) / variation) ** 2), 4)
    return move_accuracy


def move_type_func(move_accuracy):
    # best = 3, great = 2, good = 1, okay = 0, inacc = -1, mistake = -2, blunder = -3
    if move_accuracy == 1:
        move_type = 3
    elif 0.90 <= move_accuracy < 1:
        move_type = 2
    elif 0.80 <= move_accuracy < .90:
        move_type = 1
    elif 0.60 <= move_accuracy < .80:
        move_type = 0
    elif 0.40 <= move_accuracy < .60:
        move_type = -1
    elif 0.25 <= move_accuracy < .40:
        move_type = -2
    else:
        move_type = -3
    return move_type


def game_acc_calc_white(chess_game_move_acc):
    # White
    white_move_acc_list = chess_game_move_acc[::2]
    black_move_acc_list = chess_game_move_acc[1::2]
    white_move_acc_len = len(chess_game_move_acc[::2])
    black_move_acc_len = len(chess_game_move_acc[1::2])
    if white_move_acc_len == 0:
        white_game_acc = 0
    else:
        white_game_acc = round(sum(white_move_acc_list) / white_move_acc_len * 100, 2)
    if black_move_acc_len == 0:
        black_game_acc = 0
    else:
        black_game_acc = round(sum(black_move_acc_list) / black_move_acc_len * 100, 2)
    return white_game_acc


def game_acc_calc_black(chess_game_move_acc):
    # Black
    black_move_acc_list = chess_game_move_acc[1::2]
    black_move_acc_len = len(chess_game_move_acc[1::2])
    if black_move_acc_len == 0:
        black_game_acc = 0
    else:
        black_game_acc = round(sum(black_move_acc_list) / black_move_acc_len * 100, 2)
    return black_game_acc


def game_phase_acc_calc(chess_game_move_acc):
    global ow, mw, ew, ob, mb, eb
       # White
    list_w = chess_game_move_acc[::2]
    list_w_split = np.array_split(list_w, 3)
    for array in list_w_split:
        list_w_o = list_w_split[0]
        list_w_m = list_w_split[1]
        list_w_e = list_w_split[2]
        len_lwo, len_lwm, len_lwe = len(list_w_o), len(list_w_m), len(list_w_e)
        if len_lwo == 0:
            ow = 0
        else:
            ow = round(sum(list_w_o) / len_lwo * 100, 2)
        if len_lwm == 0:
            mw = 0
        else:
            mw = round(sum(list_w_m) / len_lwm * 100, 2)
        if len_lwe == 0:
            ew = 0
        else:
            ew = round(sum(list_w_e) / len_lwe * 100, 2)
            # Black
    list_b = chess_game_move_acc[1::2]
    list_b_split = np.array_split(list_b, 3)
    for array in list_b_split:
        list_b_o = list_b_split[0]
        list_b_m = list_b_split[1]
        list_b_e = list_b_split[2]
        len_lbo, len_lbm, len_lbe = len(list_b_o), len(list_b_m), len(list_b_e)
        if len_lbo == 0:
            ob = 0
        else:
            ob = round(sum(list_b_o) / len_lbo * 100, 2)
        if len_lbm == 0:
            mb = 0
        else:
            mb = round(sum(list_b_m) / len_lbm * 100, 2)
        if len_lbe == 0:
            eb = 0
        else:
            eb = round(sum(list_b_e) / len_lbe * 100, 2)
    return ow, mw, ew, ob, mb, eb


def game_section_improvement_white(ow, mw, ew):
    # White
    if ow < mw and ow < ew:
        improvement_white = 0
    elif mw < ow and mw < ew:
        improvement_white = 1
    else:
        improvement_white = 2
    return improvement_white


def game_section_improvement_black(ob, mb, eb):
    # black
    if ob < mb and ob < eb:
        improvement_black = 0
    elif mb < ob and mb < eb:
        improvement_black = 1
    else:
        improvement_black = 2
    return improvement_black


def sum_move_type(chess_game_move_type):
    global w_best, b_best, w_great, b_great, w_good, b_good, w_ok, b_ok, w_inaccuracy, b_inaccuracy, w_mistake, b_mistake, w_blunder, b_blunder
    # Best
    w_best = chess_game_move_type[::2].count(3)
    b_best = chess_game_move_type[1::2].count(3)
    # Great
    w_great = chess_game_move_type[::2].count(2)
    b_great = chess_game_move_type[1::2].count(2)
    # Good
    w_good = chess_game_move_type[::2].count(1)
    b_good = chess_game_move_type[1::2].count(1)
    # Ok
    w_ok = chess_game_move_type[::2].count(0)
    b_ok = chess_game_move_type[1::2].count(0)
    # Inaccuracy
    w_inaccuracy = chess_game_move_type[::2].count(-1)
    b_inaccuracy = chess_game_move_type[1::2].count(-1)
    # Mistake
    w_mistake = chess_game_move_type[::2].count(-2)
    b_mistake = chess_game_move_type[1::2].count(-2)
    # Blunder
    w_blunder = chess_game_move_type[::2].count(-3)
    b_blunder = chess_game_move_type[1::2].count(-3)
    return w_best, b_best, w_great, b_great, w_good, b_good, w_ok, b_ok, w_inaccuracy, b_inaccuracy, w_mistake, b_mistake, w_blunder, b_blunder

def rerun_filter():
    logging.basicConfig(filename =file_logger, format='[%(levelname)s %(module)s] %(asctime)s - %(message)s', level = logging.INFO, datefmt='%Y/%m/%d %I:%M:%S')
    logger = logging.getLogger(__name__)
    game_number = 0

    with open(file_logger,"r") as log_file:
        lines = log_file.readlines()

    if not lines:
        with open(file_logger,"w") as f:
            init_dt = datetime.strptime("2000-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
            logger.info(f"DateTime of last game entry | {init_dt} | {game_number}")
    else:
        llog = lines[-1]
        llog_date_str = llog.split("|")[1].strip()
        llog_date = datetime.strptime(llog_date_str, '%Y-%m-%d %H:%M:%S')
        return llog_date    


def clean_rerun_files():
    file_exists = exists(file_move_data)

    if file_exists:
        pass
    else:
        init_file = pd.DataFrame(list())
        init_file.to_csv(file_move_data)

    with open(file_logger,"r") as log_file:
        lines = log_file.readlines()

    if not lines:
        pass
    else:
        if file_exists:
            llog = lines[-1]
            llog_gn = int(int(llog.split("|")[2].strip())+1)
            col_names = ["Date","Game_number","Engine_Depth","Game_date","Move_number",
                         "Move","Best_move","Move_eval","Best_move_eval","Move_eval_diff",
                         "Move accuracy","Move_type"]
            unclean_df = pd.read_csv(file_move_data, names=col_names)
            df_filter = unclean_df["Game_number"] != llog_gn
            clean_df = unclean_df[df_filter]
            clean_df.to_csv(file_move_data, mode="w", index=False, header=False)
        else:
            pass

    

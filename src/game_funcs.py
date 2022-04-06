import numpy as np


def w_accuracy(chess_game_move_acc):
    '''
    stuff
    '''
    # White
    white_move_acc_list = chess_game_move_acc[::2]
    white_move_acc_len = len(chess_game_move_acc[::2])
    if white_move_acc_len == 0:
        white_game_acc = 0
    else:
        white_game_acc = round(sum(white_move_acc_list) / white_move_acc_len * 100, 2)
    return white_game_acc


def b_accuracy(chess_game_move_acc):
    '''
    stuff
    '''
    # Black
    black_move_acc_list = chess_game_move_acc[1::2]
    black_move_acc_len = len(chess_game_move_acc[1::2])
    if black_move_acc_len == 0:
        black_game_acc = 0
    else:
        black_game_acc = round(sum(black_move_acc_list) / black_move_acc_len * 100, 2)
    return black_game_acc


def phase_accuracy(chess_game_move_acc):
    '''
    stuff
    '''
    global ow, mw, ew, ob, mb, eb
    # White
    list_w = chess_game_move_acc[::2]
    list_w_split = np.array_split(list_w, 3)
    for _ in list_w_split:
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
    for _ in list_b_split:
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
    '''
    stuff
    '''
    # White
    if ow < mw and ow < ew:
        improvement_white = 0
    elif mw < ow and mw < ew:
        improvement_white = 1
    else:
        improvement_white = 2
    return improvement_white


def game_section_improvement_black(ob, mb, eb):
    '''
    stuff
    '''
    # black
    if ob < mb and ob < eb:
        improvement_black = 0
    elif mb < ob and mb < eb:
        improvement_black = 1
    else:
        improvement_black = 2
    return improvement_black
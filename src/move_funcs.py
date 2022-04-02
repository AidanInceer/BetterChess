import math


def move_eval(eval_move_init):
    '''
    stuff
    '''
    get_eval_best_move = str(eval_move_init['score'].white())
    if "#" in get_eval_best_move:
        get_eval_best_move = get_eval_best_move[1:]
    else:
        get_eval_best_move = get_eval_best_move
    get_eval_best_move = int(get_eval_best_move)
    return get_eval_best_move


def eval_diff(move_num, get_eval_best_move, get_eval_mainline):
    '''
    stuff
    '''
    # Calculation of eval diff
    if move_num % 2 == 0:
        # Calculation of move accuracy for white
        eval_diff = round(abs(get_eval_best_move - get_eval_mainline), 3)
        return eval_diff
    else:
        # Calculation of move accuracy for black
        eval_diff = round(abs(get_eval_mainline - get_eval_best_move), 3)
        return eval_diff


def move_acc(eval_diff):
    '''
    stuff
    '''
    m, v = 0, 0.75
    move_acc = round(math.exp(-0.00005*((eval_diff-m)/v)**2), 4)
    return move_acc


def move_type(move_acc):
    '''
    stuff
    '''
    # best = 3, great = 2, good = 1, okay = 0
    # inacc = -1, mistake = -2, blunder = -3
    if move_acc == 1:
        move_type = 3
    elif 0.90 <= move_acc < 1:
        move_type = 2
    elif 0.80 <= move_acc < .90:
        move_type = 1
    elif 0.60 <= move_acc < .80:
        move_type = 0
    elif 0.40 <= move_acc < .60:
        move_type = -1
    elif 0.25 <= move_acc < .40:
        move_type = -2
    else:
        move_type = -3
    return move_type


def sum_move_type(chess_game_move_type):
    '''
    stuff
    '''
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

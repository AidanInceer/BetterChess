import math


def move_eval(eval_move_init):
    '''Returns the evalaution if the best move were played.'''
    get_eval_best_move = str(eval_move_init['score'].white())
    if "#" in get_eval_best_move:
        get_eval_best_move = get_eval_best_move[1:]
    else:
        get_eval_best_move = get_eval_best_move
    get_eval_best_move = int(get_eval_best_move)
    return get_eval_best_move


def eval_diff(move_num, get_eval_best_move, get_eval_mainline):
    '''Returns the eval difference between the best and mainline move.'''
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
    '''Returns the move accuracy for a given move.'''
    m, v = 0, 0.75
    move_acc = round(math.exp(-0.00005*((eval_diff-m)/v)**2), 4)
    return move_acc


def move_type(move_acc):
    '''Returns the move type for a given move.'''
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


def sum_best_mv(move_type_list):
    '''Returns the number of best moves for black and white.'''
    w_best = move_type_list[::2].count(3)
    b_best = move_type_list[1::2].count(3)
    return w_best, b_best


def sum_great_mv(move_type_list):
    '''Returns the number of great moves for black and white.'''
    w_good = move_type_list[::2].count(1)
    b_good = move_type_list[1::2].count(1)
    return w_good, b_good


def sum_good_mv(move_type_list):
    '''Returns the number of good moves for black and white.'''
    w_good = move_type_list[::2].count(1)
    b_good = move_type_list[1::2].count(1)
    return w_good, b_good


def sum_ok_mv(move_type_list):
    '''Returns the number of ok moves for black and white.'''
    w_ok = move_type_list[::2].count(0)
    b_ok = move_type_list[1::2].count(0)
    return w_ok, b_ok


def sum_inac_mv(move_type_list):
    '''Returns the number of innaccurate moves for black and white.'''
    w_inaccuracy = move_type_list[::2].count(-1)
    b_inaccuracy = move_type_list[1::2].count(-1)
    return w_inaccuracy, b_inaccuracy


def sum_mist_mv(move_type_list):
    '''Returns the number of mistakes for black and white.'''
    w_mistake = move_type_list[::2].count(-2)
    b_mistake = move_type_list[1::2].count(-2)
    return w_mistake, b_mistake


def sum_blndr_mv(move_type_list):
    '''Returns the number of blunders for black and white.'''
    w_blunder = move_type_list[::2].count(-3)
    b_blunder = move_type_list[1::2].count(-3)
    return w_blunder, b_blunder

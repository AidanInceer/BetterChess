import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from betterchess.core.game import Game, Prepare


def test_game_time_of_day_night():
    game_datetime = datetime(2022, 5, 29, 4, 35, 47)
    assert Game.game_time_of_day(game_datetime) == "Night"


def test_game_time_of_day_morning():
    game_datetime = datetime(2022, 5, 29, 9, 35, 47)
    assert Game.game_time_of_day(game_datetime) == "Morning"


def test_game_time_of_day_afternoon():
    game_datetime = datetime(2022, 5, 29, 13, 35, 47)
    assert Game.game_time_of_day(game_datetime) == "Afternoon"


def test_game_time_of_day_evening():
    game_datetime = datetime(2022, 5, 29, 19, 35, 47)
    assert Game.game_time_of_day(game_datetime) == "Evening"


def test_game_day_of_week():
    game_datetime = datetime(2022, 5, 29, 19, 35, 47)
    assert Game.game_day_of_week(game_datetime) == "Sunday"


def test_game_w_acc():
    game_move_acc = [90, 80, 90, 80, 90, 80]
    assert Game.game_w_acc(game_move_acc) == 90


def test_game_w_acc_zero():
    game_move_acc = []
    assert Game.game_w_acc(game_move_acc) == 0


def test_game_b_acc():
    game_move_acc = [90, 80, 90, 80, 90, 80]
    assert Game.game_b_acc(game_move_acc) == 80


def test_game_b_acc_zero():
    game_move_acc = []
    assert Game.game_b_acc(game_move_acc) == 0


def test_op_w_acc():
    game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
    assert Game.op_w_acc(game_move_acc) == 90


def test_op_w_acc_zero():
    game_move_acc = []
    assert Game.op_w_acc(game_move_acc) == 0


def test_mid_w_acc():
    game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
    assert Game.mid_w_acc(game_move_acc) == 30


def test_mid_w_acc_zero():
    game_move_acc = []
    assert Game.mid_w_acc(game_move_acc) == 0


def test_end_w_acc():
    game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
    assert Game.end_w_acc(game_move_acc) == 70


def test_end_w_acc_zero():
    game_move_acc = []
    assert Game.end_w_acc(game_move_acc) == 0


def test_op_b_acc():
    game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
    assert Game.op_b_acc(game_move_acc) == 80


def test_op_b_acc_zero():
    game_move_acc = []
    assert Game.op_b_acc(game_move_acc) == 0


def test_mid_b_acc():
    game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
    assert Game.mid_b_acc(game_move_acc) == 20


def test_mid_b_acc_zero():
    game_move_acc = []
    assert Game.mid_b_acc(game_move_acc) == 0


def test_end_b_acc():
    game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
    assert Game.end_b_acc(game_move_acc) == 60


def test_end_b_acc_zero():
    game_move_acc = []
    assert Game.end_b_acc(game_move_acc) == 0


def test_w_sec_imp_opening():
    ow, mw, ew = 80.0, 90.0, 90.0
    assert Game.w_sec_imp(ow, mw, ew) == "Opening"


def test_w_sec_imp_midgame():
    ow, mw, ew = 90.0, 80.0, 90.0
    assert Game.w_sec_imp(ow, mw, ew) == "Midgame"


def test_w_sec_imp_endgame():
    ow, mw, ew = 90.0, 90.0, 80.0
    assert Game.w_sec_imp(ow, mw, ew) == "Endgame"


def test_b_sec_imp_opening():
    ob, mb, eb = 80.0, 90.0, 90.0
    assert Game.b_sec_imp(ob, mb, eb) == "Opening"


def test_b_sec_imp_midgame():
    ob, mb, eb = 90.0, 80.0, 90.0
    assert Game.b_sec_imp(ob, mb, eb) == "Midgame"


def test_b_sec_imp_endgame():
    ob, mb, eb = 90.0, 90.0, 80.0
    assert Game.b_sec_imp(ob, mb, eb) == "Endgame"


def test_white_castle_move_num():
    white_castle_num = [0, 0, 0, 15]
    assert Game.white_castle_move_num(white_castle_num) == 15


def test_black_castle_move_num():
    black_castle_num = [0, 0, 0, 31]
    assert Game.black_castle_move_num(black_castle_num) == 31


def test_has_white_castled_yes():
    white_castle_num = [0, 0, 0, 1]
    assert Game.has_white_castled(white_castle_num) == 1


def test_has_white_castled_no():
    white_castle_num = [0, 0, 0, 0]
    assert Game.has_white_castled(white_castle_num) == 0


def test_has_black_castled_yes():
    black_castle_num = [0, 0, 0, 2]
    assert Game.has_black_castled(black_castle_num) == 1


def test_has_black_castled_no():
    black_castle_num = [0, 0, 0, 0]
    assert Game.has_black_castled(black_castle_num) == 0


def test_white_castle_phase_opening():
    white_castle_num = [0, 1]
    total_moves = 10
    assert Game.white_castle_phase(white_castle_num, total_moves) == "Opening"


def test_white_castle_phase_midgame():
    white_castle_num = [0, 0, 0, 0, 5]
    total_moves = 10
    assert Game.white_castle_phase(white_castle_num, total_moves) == "Midgame"


def test_white_castle_phase_endgame():
    white_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 9]
    total_moves = 10
    assert Game.white_castle_phase(white_castle_num, total_moves) == "Endgame"


def test_white_castle_phase_none():
    white_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total_moves = 10
    assert Game.white_castle_phase(white_castle_num, total_moves) == "None"


def test_white_castle_phase_totnone():
    white_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total_moves = 0
    assert Game.white_castle_phase(white_castle_num, total_moves) == "None"


def test_black_castle_phase_opening():
    black_castle_num = [0, 1]
    total_moves = 10
    assert Game.black_castle_phase(black_castle_num, total_moves) == "Opening"


def test_black_castle_phase_midgame():
    black_castle_num = [0, 0, 0, 0, 5]
    total_moves = 10
    assert Game.black_castle_phase(black_castle_num, total_moves) == "Midgame"


def test_black_castle_phase_endgame():
    black_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 9]
    total_moves = 10
    assert Game.black_castle_phase(black_castle_num, total_moves) == "Endgame"


def test_black_castle_phase_none():
    black_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total_moves = 10
    assert Game.black_castle_phase(black_castle_num, total_moves) == "None"


def test_black_castle_phase_totnone():
    black_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total_moves = 0
    assert Game.black_castle_phase(black_castle_num, total_moves) == "None"

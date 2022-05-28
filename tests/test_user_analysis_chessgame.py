from src.user_analysis import ChessGame
import chess
import pandas as pd
import unittest
from src.user_analysis import ChessMove
from src.user_analysis import ChessGameHeaders
from unittest import mock
from pandas.testing import assert_frame_equal
from chess import WHITE
from chess.engine import PovScore, Cp, Mate
from chess.pgn import read_game


class TestGame:
    def test_run_game_analysis(self):
        pass

    def test_init_game_analysis(self):
        pass

    def test_analyse_game(self):
        pass

    def test_init_game(self):
        pass

    def test_init_board(self):
        pass

    def test_init_game_lists(self):
        pass

    def test_game_analysis_filter(self):
        pass

    def test_sum_move_types(self):
        pass

    def test_user_game_data(self):
        pass

    def test_export_game_data(self):
        pass

    def test_game_time_of_day(self):
        pass

    def test_game_day_of_week(self):
        pass

    def test_white_castle_move_num(self):
        pass

    def test_black_castle_move_num(self):
        pass

    def test_has_white_castled(self):
        pass

    def test_has_black_castled(self):
        pass

    def test_white_castle_phase(self):
        pass

    def test_black_castle_phase(self):
        pass

    def test_game_w_acc(self):
        pass

    def test_game_b_acc(self):
        pass

    def test_op_w_acc(self):
        pass

    def test_mid_w_acc(self):
        pass

    def test_end_w_acc(self):
        pass

    def test_op_b_acc(self):
        pass

    def test_mid_b_acc(self):
        pass

    def test_end_b_acc(self):
        pass

    def test_w_sec_imp(self):
        pass

    def test_b_sec_imp(self):
        pass

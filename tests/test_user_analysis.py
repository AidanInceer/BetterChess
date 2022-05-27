from src.user_analysis import ChessMove
from unittest import mock
from pandas.testing import assert_frame_equal
import pandas as pd
import unittest


class BaseFileHandler():
    def __init__(self):
        self.move_data = r"./test_move_data.csv"


class TestUser():
    pass


class TestGame():
    pass


class TestMove(unittest.TestCase):
    def test_mainline_move(self):
        pass

    def test_best_move(self):
        pass

    def test_move_eval(self):
        pass

    def test_eval_delta_white(self):
        move_num, eval_bm, eval_ml = 2, 200, 20
        assert ChessMove.eval_delta(
            self,
            move_num,
            eval_bm,
            eval_ml) == 180

    def test_eval_delta_black(self):
        move_num, eval_bm, eval_ml = 2, 20, 20
        assert ChessMove.eval_delta(
            self,
            move_num,
            eval_bm,
            eval_ml) == 0

    def test_move_accuracy(self):
        ed = 100
        assert ChessMove.move_accuracy(self, ed) == 87.5

    def test_assign_move_type_p2(self):
        move_acc = 100
        assert ChessMove.assign_move_type(self, move_acc) == 2

    def test_assign_move_type_p1(self):
        move_acc = 99.7
        assert ChessMove.assign_move_type(self, move_acc) == 1

    def test_assign_move_type_p0(self):
        move_acc = 90
        assert ChessMove.assign_move_type(self, move_acc) == 0

    def test_assign_move_type_n1(self):
        move_acc = 60
        assert ChessMove.assign_move_type(self, move_acc) == -1

    def test_assign_move_type_n2(self):
        move_acc = 35
        assert ChessMove.assign_move_type(self, move_acc) == -2

    def test_assign_move_type_n3(self):
        move_acc = 20
        assert ChessMove.assign_move_type(self, move_acc) == -3

    def test_assign_move_type_n4(self):
        move_acc = 0
        assert ChessMove.assign_move_type(self, move_acc) == -4

    def test_get_piece_square_int(self):
        move = "a1a2"
        assert ChessMove.get_piece_square_int(self, move) == 8

    def test_chess_piece(self):
        # move = "e2e4"
        # assert ChessMove.chess_piece(self, move) == "pawn"
        pass

    def test_move_colour(self):
        pass

    def test_castling_type(self):
        pass

    def test_white_castle_move_num(self):
        pass

    def test_black_castle_move_num(self):
        pass

    def test_get_time_spent_on_move(self) -> float:
        pass

    def test_filter_timecont_header_interval(self):
        tc_white = "180+5"
        tc_black = "180+5"
        assert ChessMove.filter_timecont_header(
            self,
            tc_white,
            tc_black) == (180, 180, 5)

    def test_filter_timecont_header(self):
        tc_white = "100"
        tc_black = "100"
        assert ChessMove.filter_timecont_header(
            self,
            tc_white,
            tc_black) == (100, 100, 0)

    def test_create_move_df(self):
        test_move_df = pd.DataFrame({
            "Username": "Ainceer",
            "Game_date": "2020-11-01 00:00:00",
            "edepth": 10,
            "Game_number": 1,
            "Move_number": 1,
            "Move": "e2e4",
            "Move_eval": 1,
            "Best_move": "e2e4",
            "Best_move_eval": 1,
            "Move_eval_diff": 0,
            "Move accuracy": 100,
            "Move_type": 2,
            "Piece": "pawn",
            "Move_colour": "white",
            "Castling_type": None,
            "White_castle_num": 0,
            "Black_castle_num": 0,
            "Move_time": 10
            }, index=[0])
        assert_frame_equal(test_move_df, ChessMove.create_move_df(
            self, "Ainceer", "2020-11-01 00:00:00", 10, 1,
            1, "e2e4", 1, "e2e4", 1, 0, 100, 2,
            "pawn", "white", None, 0, 0, 10))

    def test_export_move_data(self):
        self.file_paths = BaseFileHandler()
        self.file_paths.move_data = r"test.csv"
        self.username = "Ainceer"

        self.test_df = pd.DataFrame({
            "Username": self.username
            }, index=[0])
        with mock.patch.object(self.test_df, "to_csv") as to_csv_mock:
            ChessMove.export_move_data(
                self,
                self.file_paths.move_data,
                self.test_df)
            to_csv_mock.assert_called_with(
                'test.csv',
                mode='a',
                header=False,
                index=False)

    def test_append_to_game_lists(self) -> None:
        pass

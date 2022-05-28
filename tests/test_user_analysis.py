from src.user_analysis import ChessMove
from unittest import mock
from pandas.testing import assert_frame_equal
import pandas as pd
import unittest
from chess.engine import PovScore, Cp, Mate
from chess import WHITE
from chess.pgn import Headers
import chess


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
        move = {'score': PovScore(Cp(10), WHITE)}
        assert 10 == ChessMove.move_eval(self, move)

    def test_move_eval_mate(self):
        move = {'score': PovScore(Mate(-0), WHITE)}
        assert 0 == ChessMove.move_eval(self, move)

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

    def test_chess_piece_pawn(self):
        curr_board = chess.BaseBoard()
        square_int = 8
        assert "pawn" == ChessMove.chess_piece(self, curr_board, square_int)

    def test_chess_piece_knight(self):
        curr_board = chess.BaseBoard()
        square_int = 1
        assert "knight" == ChessMove.chess_piece(self, curr_board, square_int)

    def test_chess_piece_bishop(self):
        curr_board = chess.BaseBoard()
        square_int = 2
        assert "bishop" == ChessMove.chess_piece(self, curr_board, square_int)

    def test_chess_piece_rook(self):
        curr_board = chess.BaseBoard()
        square_int = 0
        assert "rook" == ChessMove.chess_piece(self, curr_board, square_int)

    def test_chess_piece_queen(self):
        curr_board = chess.BaseBoard()
        square_int = 3
        assert "queen" == ChessMove.chess_piece(self, curr_board, square_int)

    def test_chess_piece_king(self):
        curr_board = chess.BaseBoard()
        square_int = 4
        assert "king" == ChessMove.chess_piece(self, curr_board, square_int)

    def test_chess_piece_none(self):
        curr_board = chess.BaseBoard()
        square_int = 32
        assert " " == ChessMove.chess_piece(self, curr_board, square_int)

    def test_move_colour_white(self):
        move_num = 2
        assert ChessMove.move_colour(self, move_num) == "white"

    def test_move_colour_black(self):
        move_num = 3
        assert ChessMove.move_colour(self, move_num) == "black"

    def test_castling_type_ws(self):
        piece = "king"
        move_col = "white"
        str_ml = "e1g1"
        assert "white_short" == ChessMove.castling_type(
            self, piece, move_col, str_ml)

    def test_castling_type_wl(self):
        piece = "king"
        move_col = "white"
        str_ml = "e1c1"
        assert "white_long" == ChessMove.castling_type(
            self, piece, move_col, str_ml)

    def test_castling_type_bs(self):
        piece = "king"
        move_col = "black"
        str_ml = "e8g8"
        assert "black_short" == ChessMove.castling_type(
            self, piece, move_col, str_ml)

    def test_castling_type_bl(self):
        piece = "king"
        move_col = "black"
        str_ml = "e8c8"
        assert "black_long" == ChessMove.castling_type(
            self, piece, move_col, str_ml)

    def test_castling_type_none(self):
        piece = "pawn"
        move_col = "white"
        str_ml = "e1g1"
        assert ChessMove.castling_type(self, piece, move_col, str_ml) is None

    def test_white_castle_move_num_y(self):
        castle_type = "white_short"
        move_num = 10
        assert ChessMove.white_castle_move_num(
            self, castle_type, move_num) == 10

    def test_white_castle_move_num_n(self):
        castle_type = None
        move_num = 10
        assert ChessMove.white_castle_move_num(
            self, castle_type, move_num) == 0

    def test_black_castle_move_num_y(self):
        castle_type = "black_short"
        move_num = 10
        assert ChessMove.black_castle_move_num(
            self, castle_type, move_num) == 10

    def test_black_castle_move_num_n(self):
        castle_type = None
        move_num = 10
        assert ChessMove.black_castle_move_num(
            self, castle_type, move_num) == 0

    def test_get_time_spent_on_move_white(self) -> float:
        self.file_path = BaseFileHandler().temp
        move_num = 2
        timers = (600, 600, 0)
        assert 2.7 == ChessMove.get_time_spent_on_move(
            self, self.file_path, move_num, timers)

    def test_get_time_spent_on_move_black(self) -> float:
        self.file_path = BaseFileHandler().temp
        move_num = 3
        timers = (600, 600, 0)
        assert 5.1 == ChessMove.get_time_spent_on_move(
            self, self.file_path, move_num, timers)

    def test_filter_timecont_header(self):
        self.file_path = BaseFileHandler().temp
        assert ChessMove.filter_timecont_header(
            self,
            self.file_path) == (600, 600, 0)

    def test_filter_timecont_header_interval(self):
        self.file_path = BaseFileHandler().temp2
        assert ChessMove.filter_timecont_header(
            self,
            self.file_path) == (180, 180, 5)

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


class TestGameHeaders(unittest.TestCase):
    def test_collect_headers(self):
        pass

    def test_time_control(self):
        pass

    def test_player_white(self):
        pass

    def test_player_black(self):
        pass

    def test_user_colour(self):
        pass

    def test_rating_white(self):
        pass

    def test_test_rating_black(self):
        pass

    def test_opening_cls(self):
        pass

    def test_opening_nm(self):
        pass

    def test_game_termination(self):
        pass

    def test_rating_user(self):
        pass

    def test_rating_opponent(self):
        pass

    def test_win_draw_loss(self):
        pass

    def test_user_winr(self):
        pass

    def test_game_dt(self):
        pass

    def test_game_t(self):
        pass

    def test_game_dt_time(self):
        pass


class BaseFileHandler():
    def __init__(self):
        self.move_data = r"./test_move_data.csv"
        self.temp = r"tests/test.pgn"
        self.temp2 = r"tests/test2.pgn"

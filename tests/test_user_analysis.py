import chess
import pandas as pd
import unittest
from chess import WHITE
from chess.engine import PovScore, Cp, Mate
from chess.pgn import read_game
from datetime import datetime
from pandas.testing import assert_frame_equal
from src.user_analysis import ChessGame
from src.user_analysis import ChessMove
from src.user_analysis import ChessGameHeaders
from unittest.mock import patch
from unittest import mock


class TestUser:
    def test_create_logger(self):
        pass

    def test_create_engine(self):
        pass

    def test_run_analysis(self):
        pass

    def test_analyse_user(self):
        pass

    def test_init_all_games(self):
        pass

    def test_write_temp_pgn(self):
        pass


class TestGame:
    def test_run_game_analysis(self):
        pass

    def test_init_game_analysis(self):
        pass

    def test_analyse_game(self):
        pass

    def test_init_game(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        ob1 = isinstance(chess_game, chess.Board)
        ob2 = isinstance(ChessGame.init_game(self, tempfilepath), chess.Board)
        assert ob1 == ob2

    def test_init_board(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGame.init_board(self, chess_game) == chess_game.board()

    def test_init_game_lists(self):
        pass

    def test_game_analysis_filter(self):
        tempfilepath = BaseFileHandler().logpath
        game_dt = datetime(2020, 11, 8, 23, 10, 17)
        assert ChessGame.game_analysis_filter(self, tempfilepath) == game_dt

    def test_sum_move_types_none(self):
        move_type_list = []
        test_dict = {
            "Num_w_best": 0,
            "Num_b_best": 0,
            "Num_w_excl": 0,
            "Num_b_excl": 0,
            "Num_w_good": 0,
            "Num_b_good": 0,
            "Num_w_inac": 0,
            "Num_b_inac": 0,
            "Num_w_mist": 0,
            "Num_b_mist": 0,
            "Num_w_blun": 0,
            "Num_b_blun": 0,
            "Num_w_misw": 0,
            "Num_b_misw": 0,
        }
        assert ChessGame.sum_move_types(self, move_type_list) == test_dict
        pass


    @patch("src.user_analysis.ChessGame.game_time_of_day")
    @patch("src.user_analysis.ChessGame.game_day_of_week")
    @patch("src.user_analysis.ChessGame.game_w_acc")
    @patch("src.user_analysis.ChessGame.op_w_acc")
    @patch("src.user_analysis.ChessGame.mid_w_acc")
    @patch("src.user_analysis.ChessGame.end_w_acc")
    @patch("src.user_analysis.ChessGame.w_sec_imp")
    @patch("src.user_analysis.ChessGame.white_castle_move_num")
    @patch("src.user_analysis.ChessGame.black_castle_move_num")
    @patch("src.user_analysis.ChessGame.has_white_castled")
    @patch("src.user_analysis.ChessGame.has_black_castled")
    @patch("src.user_analysis.ChessGame.white_castle_phase")
    @patch("src.user_analysis.ChessGame.black_castle_phase")
    def test_user_game_data(self, mock_gtod, mock_gdow, gwa, owa, mow, eow,
                            wsi, wcmn, bcmn, hwc, hbc, wcp, bcp):
        mock_gtod.return_value = 1
        mock_gdow.return_value = 1
        gwa.return_value = 1
        owa.return_value = 1
        mow.return_value = 1
        eow.return_value = 1
        wsi.return_value = 1
        wcmn.return_value = 1
        bcmn.return_value = 1
        hwc.return_value = 1
        hbc.return_value = 1
        wcp.return_value = 1
        bcp.return_value = 1
        
        

    def test_export_game_data(self):
        pass

    def test_game_time_of_day(self):
        game_datetime = datetime(2022, 5, 29, 19, 35, 47)
        assert ChessGame.game_time_of_day(self, game_datetime) == "Evening"

    def test_game_day_of_week(self):
        game_datetime = datetime(2022, 5, 29, 19, 35, 47)
        assert ChessGame.game_day_of_week(self, game_datetime) == "Sunday"

    def test_game_w_acc(self):
        game_move_acc = [90, 80, 90, 80, 90, 80]
        assert ChessGame.game_w_acc(self, game_move_acc) == 90

    def test_game_w_acc_zero(self):
        game_move_acc = []
        assert ChessGame.game_w_acc(self, game_move_acc) == 0

    def test_game_b_acc(self):
        game_move_acc = [90, 80, 90, 80, 90, 80]
        assert ChessGame.game_b_acc(self, game_move_acc) == 80

    def test_game_b_acc_zero(self):
        game_move_acc = []
        assert ChessGame.game_b_acc(self, game_move_acc) == 0

    def test_op_w_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert ChessGame.op_w_acc(self, game_move_acc) == 90

    def test_op_w_acc_zero(self):
        game_move_acc = []
        assert ChessGame.op_w_acc(self, game_move_acc) == 0

    def test_mid_w_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert ChessGame.mid_w_acc(self, game_move_acc) == 30

    def test_mid_w_acc_zero(self):
        game_move_acc = []
        assert ChessGame.mid_w_acc(self, game_move_acc) == 0

    def test_end_w_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert ChessGame.end_w_acc(self, game_move_acc) == 70

    def test_end_w_acc_zero(self):
        game_move_acc = []
        assert ChessGame.end_w_acc(self, game_move_acc) == 0

    def test_op_b_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert ChessGame.op_b_acc(self, game_move_acc) == 80

    def test_op_b_acc_zero(self):
        game_move_acc = []
        assert ChessGame.op_b_acc(self, game_move_acc) == 0

    def test_mid_b_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert ChessGame.mid_b_acc(self, game_move_acc) == 20

    def test_mid_b_acc_zero(self):
        game_move_acc = []
        assert ChessGame.mid_b_acc(self, game_move_acc) == 0

    def test_end_b_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert ChessGame.end_b_acc(self, game_move_acc) == 60

    def test_end_b_acc_zero(self):
        game_move_acc = []
        assert ChessGame.end_b_acc(self, game_move_acc) == 0

    def test_w_sec_imp_opening(self):
        ow, mw, ew = 80.0, 90.0, 90.0
        assert ChessGame.w_sec_imp(self, ow, mw, ew) == "Opening"

    def test_w_sec_imp_midgame(self):
        ow, mw, ew = 90.0, 80.0, 90.0
        assert ChessGame.w_sec_imp(self, ow, mw, ew) == "Midgame"

    def test_w_sec_imp_endgame(self):
        ow, mw, ew = 90.0, 90.0, 80.0
        assert ChessGame.w_sec_imp(self, ow, mw, ew) == "Endgame"

    def test_b_sec_imp_opening(self):
        ob, mb, eb = 80.0, 90.0, 90.0
        assert ChessGame.b_sec_imp(self, ob, mb, eb) == "Opening"

    def test_b_sec_imp_midgame(self):
        ob, mb, eb = 90.0, 80.0, 90.0
        assert ChessGame.b_sec_imp(self, ob, mb, eb) == "Midgame"

    def test_b_sec_imp_endgame(self):
        ob, mb, eb = 90.0, 90.0, 80.0
        assert ChessGame.b_sec_imp(self, ob, mb, eb) == "Endgame"

    def test_white_castle_move_num(self):
        white_castle_num = [0, 0, 0, 15]
        assert ChessGame.white_castle_move_num(self, white_castle_num) == 15

    def test_black_castle_move_num(self):
        black_castle_num = [0, 0, 0, 31]
        assert ChessGame.black_castle_move_num(self, black_castle_num) == 31

    def test_has_white_castled_yes(self):
        white_castle_num = [0, 0, 0, 1]
        assert ChessGame.has_white_castled(self, white_castle_num) == 1

    def test_has_white_castled_no(self):
        white_castle_num = [0, 0, 0, 0]
        assert ChessGame.has_white_castled(self, white_castle_num) == 0

    def test_has_black_castled_yes(self):
        black_castle_num = [0, 0, 0, 2]
        assert ChessGame.has_black_castled(self, black_castle_num) == 1

    def test_has_black_castled_no(self):
        black_castle_num = [0, 0, 0, 0]
        assert ChessGame.has_black_castled(self, black_castle_num) == 0

    def test_white_castle_phase_opening(self):
        white_castle_num = [0, 1]
        total_moves = 10
        assert (
            ChessGame.white_castle_phase(self, white_castle_num, total_moves)
            == "Opening"
        )

    def test_white_castle_phase_midgame(self):
        white_castle_num = [0, 0, 0, 0, 5]
        total_moves = 10
        assert (
            ChessGame.white_castle_phase(self, white_castle_num, total_moves)
            == "Midgame"
        )

    def test_white_castle_phase_endgame(self):
        white_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 9]
        total_moves = 10
        assert (
            ChessGame.white_castle_phase(self, white_castle_num, total_moves)
            == "Endgame"
        )

    def test_white_castle_phase_none(self):
        white_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 9]
        total_moves = 0
        assert (
            ChessGame.white_castle_phase(self, white_castle_num, total_moves) == "None"
        )

    def test_black_castle_phase_opening(self):
        black_castle_num = [0, 1]
        total_moves = 10
        assert (
            ChessGame.black_castle_phase(self, black_castle_num, total_moves)
            == "Opening"
        )

    def test_black_castle_phase_midgame(self):
        black_castle_num = [0, 0, 0, 0, 5]
        total_moves = 10
        assert (
            ChessGame.black_castle_phase(self, black_castle_num, total_moves)
            == "Midgame"
        )

    def test_black_castle_phase_endgame(self):
        black_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 9]
        total_moves = 10
        assert (
            ChessGame.black_castle_phase(self, black_castle_num, total_moves)
            == "Endgame"
        )

    def test_black_castle_phase_None(self):
        black_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 9]
        total_moves = 0
        assert (
            ChessGame.black_castle_phase(self, black_castle_num, total_moves) == "None"
        )


class TestMove(unittest.TestCase):
    def test_mainline_move(self):
        pass

    def test_best_move(self):
        pass

    def test_move_eval(self):
        move = {"score": PovScore(Cp(10), WHITE)}
        assert 10 == ChessMove.move_eval(self, move)

    def test_move_eval_mate(self):
        move = {"score": PovScore(Mate(-0), WHITE)}
        assert 0 == ChessMove.move_eval(self, move)

    def test_eval_delta_white(self):
        move_num, eval_bm, eval_ml = 2, 200, 20
        assert ChessMove.eval_delta(self, move_num, eval_bm, eval_ml) == 180

    def test_eval_delta_black(self):
        move_num, eval_bm, eval_ml = 2, 20, 20
        assert ChessMove.eval_delta(self, move_num, eval_bm, eval_ml) == 0

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
        assert "white_short" == ChessMove.castling_type(self, piece, move_col, str_ml)

    def test_castling_type_wl(self):
        piece = "king"
        move_col = "white"
        str_ml = "e1c1"
        assert "white_long" == ChessMove.castling_type(self, piece, move_col, str_ml)

    def test_castling_type_bs(self):
        piece = "king"
        move_col = "black"
        str_ml = "e8g8"
        assert "black_short" == ChessMove.castling_type(self, piece, move_col, str_ml)

    def test_castling_type_bl(self):
        piece = "king"
        move_col = "black"
        str_ml = "e8c8"
        assert "black_long" == ChessMove.castling_type(self, piece, move_col, str_ml)

    def test_castling_type_none(self):
        piece = "pawn"
        move_col = "white"
        str_ml = "e1g1"
        assert ChessMove.castling_type(self, piece, move_col, str_ml) is None

    def test_white_castle_move_num_y(self):
        castle_type = "white_short"
        move_num = 10
        assert ChessMove.white_castle_move_num(self, castle_type, move_num) == 10

    def test_white_castle_move_num_n(self):
        castle_type = None
        move_num = 10
        assert ChessMove.white_castle_move_num(self, castle_type, move_num) == 0

    def test_black_castle_move_num_y(self):
        castle_type = "black_short"
        move_num = 10
        assert ChessMove.black_castle_move_num(self, castle_type, move_num) == 10

    def test_black_castle_move_num_n(self):
        castle_type = None
        move_num = 10
        assert ChessMove.black_castle_move_num(self, castle_type, move_num) == 0

    def test_get_time_spent_on_move_white(self) -> float:
        self.file_path = BaseFileHandler().test
        move_num = 2
        timers = (600, 600, 0)
        assert 2.7 == ChessMove.get_time_spent_on_move(
            self, self.file_path, move_num, timers
        )

    def test_get_time_spent_on_move_black(self) -> float:
        self.file_path = BaseFileHandler().test
        move_num = 3
        timers = (600, 600, 0)
        assert 5.1 == ChessMove.get_time_spent_on_move(
            self, self.file_path, move_num, timers
        )

    def test_filter_timecont_header(self):
        self.file_path = BaseFileHandler().test
        assert ChessMove.filter_timecont_header(self, self.file_path) == (600, 600, 0)

    def test_filter_timecont_header_interval(self):
        self.file_path = BaseFileHandler().test2
        assert ChessMove.filter_timecont_header(self, self.file_path) == (180, 180, 5)

    def test_create_move_df(self):
        test_move_df = pd.DataFrame(
            {
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
                "Move_time": 10,
            },
            index=[0],
        )
        assert_frame_equal(
            test_move_df,
            ChessMove.create_move_df(
                self,
                "Ainceer",
                "2020-11-01 00:00:00",
                10,
                1,
                1,
                "e2e4",
                1,
                "e2e4",
                1,
                0,
                100,
                2,
                "pawn",
                "white",
                None,
                0,
                0,
                10,
            ),
        )

    def test_export_move_data(self):
        self.file_paths = BaseFileHandler()
        self.file_paths.move_data = r"test.csv"
        self.username = "Ainceer"

        self.test_df = pd.DataFrame({"Username": self.username}, index=[0])
        with mock.patch.object(self.test_df, "to_csv") as to_csv_mock:
            ChessMove.export_move_data(self, self.file_paths.move_data, self.test_df)
            to_csv_mock.assert_called_with(
                "test.csv", mode="a", header=False, index=False
            )

    def test_append_to_game_lists(self) -> None:
        pass


class TestGameHeaders(unittest.TestCase):
    def test_collect_headers(self):
        pass

    def test_time_control(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.time_control(self, chess_game) == "600"

    def test_player_white(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.player_white(self, chess_game) == "JezzaShaw"

    def test_player_black(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.player_black(self, chess_game) == "LucidKoala"

    def test_user_colour_true(self):
        white = "JezzaShaw"
        username = "JezzaShaw"
        assert ChessGameHeaders.user_colour(self, white, username) == "White"

    def test_user_colour_false(self):
        white = "JezzaShaw"
        username = "LucidKoala"
        assert ChessGameHeaders.user_colour(self, white, username) == "Black"

    def test_rating_white(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.rating_white(self, chess_game) == 1011

    def test_test_rating_black(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.rating_black(self, chess_game) == 1009

    def test_opening_cls_no_err(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.opening_cls(self, chess_game) == "A40"

    def test_opening_cls_err(self):
        tempfilepath = BaseFileHandler().test2
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.opening_cls(self, chess_game) == "000"

    def test_opening_nm(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert (
            ChessGameHeaders.opening_nm(self, chess_game)
            == "Queens Pawn Opening Mikenas Defense 2.c4 e5 3.d5"
        )

    def test_game_termination(self):
        tempfilepath = BaseFileHandler().test2
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        username = "LucidKoala"
        assert (
            ChessGameHeaders.game_termination(self, chess_game, username)
            == "Loss by resignation"
        )

    def test_rating_user(self):
        player = "LucidKoala"
        rating_w = 1011
        rating_b = 1009
        assert ChessGameHeaders.rating_user(self, player, rating_w, rating_b) == 1009

    def test_rating_opponent(self):
        player = "LucidKoala"
        rating_w = 1011
        rating_b = 1009
        assert (
            ChessGameHeaders.rating_opponent(self, player, rating_w, rating_b) == 1011
        )

    def test_win_draw_loss(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.win_draw_loss(self, chess_game) == "White"

    def test_user_winr_win(self):
        winner = "White"
        player = "White"
        assert ChessGameHeaders.user_winr(self, winner, player) == "Win"

    def test_user_winr_loss(self):
        winner = "White"
        player = "Black"
        assert ChessGameHeaders.user_winr(self, winner, player) == "Loss"

    def test_user_winr_draw(self):
        winner = "Draw"
        player = "Black"
        assert ChessGameHeaders.user_winr(self, winner, player) == "Draw"

    def test_game_dt(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.game_dt(self, chess_game) == "2021.02.22"

    def test_game_t(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.game_t(self, chess_game) == "19:35:47"

    def test_game_dt_time(self):
        game_date = "2021.02.22"
        game_time = "19:35:47"
        assert ChessGameHeaders.game_dt_time(self, game_date, game_time) == datetime(
            2021, 2, 22, 19, 35, 47
        )


class BaseFileHandler:
    def __init__(self):
        self.move_data = r"./test_move_data.csv"
        self.test = r"tests/test.pgn"
        self.test2 = r"tests/test2.pgn"
        self.logpath = r"tests/test.log"

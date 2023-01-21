import unittest
from unittest.mock import MagicMock, patch

import chess
import chess.engine
import pandas as pd
from chess import WHITE
from chess.engine import Cp, Mate, PovScore

from betterchess.core.move import Move
from betterchess.utils.handlers import EnvHandler, FileHandler, InputHandler, RunHandler


class TestMove(unittest.TestCase):
    def setUp(self):
        env_handler = EnvHandler()
        input_handler = MagicMock()
        input_handler.collect_user_inputs.return_value = ("Ainceer", 1, "2020", "11")
        file_handler = FileHandler("Ainceer")
        run_handler = RunHandler(file_handler=file_handler)
        iter_metadata = {"game_num": 1, "tot_games": 2}
        move_metadata = {"move": 1, "move_num": 1}
        game_metadata = {
            "headers": "a",
            "game_datetime": "b",
            "board": "c",
            "chess_game": "d",
            "game_lists_dict": "e",
        }
        self.move_class = Move(
            input_handler,
            file_handler,
            run_handler,
            env_handler,
            iter_metadata,
            game_metadata,
            move_metadata,
        )
        self.engine = MagicMock()
        self.board = MagicMock()
        self.move = MagicMock()
        self.move.uci = "e2e4"

        self.move_class.str_ml = "e2e4"
        self.input_handler = MagicMock()
        self.move_class.input_handler.username = "Ainceer"
        self.move_class.input_handler.edepth = 5
        self.move_class.game_metadata = {"game_datetime": "2022-01-01 12:00:00"}
        self.move_class.iter_metadata = {"game_num": 1}
        self.move_class.move_metadata = {"move_num": 1}
        self.move_class.str_ml = "e2e4"
        self.move_class.eval_ml = 10
        self.move_class.str_bm = "e7e5"
        self.move_class.eval_bm = -10
        self.move_class.evaldiff = 20
        self.move_class.move_acc = 0.5
        self.move_class.move_type = "Quiet"
        self.move_class.piece = "Pawn"
        self.move_class.move_col = "White"
        self.move_class.castle_type = "King-side"
        self.move_class.w_castle_mv_num = 1
        self.move_class.b_castle_mv_num = 0
        self.move_class.move_time = "00:01:00"

    def test_create_move_df(self):
        result = Move.create_move_df(self.move_class)

        expected = pd.DataFrame(
            {
                "Username": "Ainceer",
                "Game_date": "2022-01-01 12:00:00",
                "Engine_depth": 5,
                "Game_number": 1,
                "Move_number": 1,
                "Move": "e2e4",
                "Move_eval": 10,
                "Best_move": "e7e5",
                "Best_move_eval": -10,
                "Move_eval_diff": 20,
                "Move_accuracy": 0.5,
                "Move_type": "Quiet",
                "Piece": "Pawn",
                "Move_colour": "White",
                "Castling_type": "King-side",
                "White_castle_num": 1,
                "Black_castle_num": 0,
                "Move_time": "00:01:00",
            },
            index=[0],
        )
        pd.testing.assert_frame_equal(result, expected)

    def test_best_move(self):
        edepth = 5
        best_move = MagicMock()
        best_move.move = "e4"
        self.engine.play.return_value = best_move
        eval_bm_init = MagicMock()
        eval_bm_init.info = {"score": {"cp": 100}}
        self.engine.analyse.return_value = eval_bm_init
        self.move_class.move_eval = MagicMock(return_value=10)
        result = self.move_class.best_move(self.board, self.engine, edepth)
        self.assertEqual(result, ("e4", 10))

    def test_mainline_move(self):
        edepth = 5
        eval_ml_init = MagicMock()
        eval_ml_init.info = {"score": {"cp": 100}}
        self.engine.analyse.return_value = eval_ml_init
        self.move_class.move_eval = MagicMock(return_value=10)
        result = self.move_class.mainline_move(
            self.move.uci, self.board, self.engine, edepth
        )
        self.assertEqual(result, ("e2e4", 10))

    def test_castling_type_bl(self):
        piece = "king"
        move_col = "black"
        str_ml = "e8c8"
        assert "black_long" == Move.castling_type(piece, move_col, str_ml)

    def test_move_eval(self):
        move = {"score": PovScore(Cp(10), WHITE)}
        assert 10 == Move.move_eval(move)

    def test_move_eval_mate(self):
        move = {"score": PovScore(Mate(-0), WHITE)}
        assert 0 == Move.move_eval(move)

    def test_eval_delta_white(self):
        move_num, eval_bm, eval_ml = 2, 200, 20
        assert Move.eval_delta(move_num, eval_bm, eval_ml) == 180

    def test_eval_delta_black(self):
        move_num, eval_bm, eval_ml = 3, 20, 20
        assert Move.eval_delta(move_num, eval_bm, eval_ml) == 0

    def test_move_accuracy(self):
        ed = 100
        assert Move.move_accuracy(ed) == 87.5

    def test_assign_move_type_p2(self):
        move_acc = 100
        assert Move.assign_move_type(move_acc) == 2

    def test_assign_move_type_p1(self):
        move_acc = 99.7
        assert Move.assign_move_type(move_acc) == 1

    def test_assign_move_type_p0(self):
        move_acc = 90
        assert Move.assign_move_type(move_acc) == 0

    def test_assign_move_type_n1(self):
        move_acc = 60
        assert Move.assign_move_type(move_acc) == -1

    def test_assign_move_type_n2(self):
        move_acc = 35
        assert Move.assign_move_type(move_acc) == -2

    def test_assign_move_type_n3(self):
        move_acc = 20
        assert Move.assign_move_type(move_acc) == -3

    def test_assign_move_type_n4(self):
        move_acc = 0
        assert Move.assign_move_type(move_acc) == -4

    def test_get_piece_square_int(self):
        move = "a1a2"
        assert Move.get_piece_square_int(move) == 8

    def test_chess_piece_pawn(self):
        curr_board = chess.BaseBoard()
        square_int = 8
        assert "pawn" == Move.chess_piece(curr_board, square_int)

    def test_chess_piece_knight(self):
        curr_board = chess.BaseBoard()
        square_int = 1
        assert "knight" == Move.chess_piece(curr_board, square_int)

    def test_chess_piece_bishop(self):
        curr_board = chess.BaseBoard()
        square_int = 2
        assert "bishop" == Move.chess_piece(curr_board, square_int)

    def test_chess_piece_rook(self):
        curr_board = chess.BaseBoard()
        square_int = 0
        assert "rook" == Move.chess_piece(curr_board, square_int)

    def test_chess_piece_queen(self):
        curr_board = chess.BaseBoard()
        square_int = 3
        assert "queen" == Move.chess_piece(curr_board, square_int)

    def test_chess_piece_king(self):
        curr_board = chess.BaseBoard()
        square_int = 4
        assert "king" == Move.chess_piece(curr_board, square_int)

    def test_chess_piece_none(self):
        curr_board = chess.BaseBoard()
        square_int = 32
        assert " " == Move.chess_piece(curr_board, square_int)

    def test_move_colour_white(self):
        move_num = 2
        assert Move.move_colour(move_num) == "white"

    def test_move_colour_black(self):
        move_num = 3
        assert Move.move_colour(move_num) == "black"

    def test_castling_type_ws(self):
        piece = "king"
        move_col = "white"
        str_ml = "e1g1"
        assert "white_short" == Move.castling_type(piece, move_col, str_ml)

    def test_castling_type_wl(self):
        piece = "king"
        move_col = "white"
        str_ml = "e1c1"
        assert "white_long" == Move.castling_type(piece, move_col, str_ml)

    def test_castling_type_bs(self):
        piece = "king"
        move_col = "black"
        str_ml = "e8g8"
        assert "black_short" == Move.castling_type(piece, move_col, str_ml)

    def test_castling_type_bl(self):
        piece = "king"
        move_col = "black"
        str_ml = "e8c8"
        assert "black_long" == Move.castling_type(piece, move_col, str_ml)

    def test_castling_type_none(self):
        piece = "pawn"
        move_col = "white"
        str_ml = "e1g1"
        assert Move.castling_type(piece, move_col, str_ml) is None

    def test_white_castle_move_num_y(self):
        castle_type = "white_short"
        move_num = 10
        assert Move.white_castle_move_num(castle_type, move_num) == 10

    def test_white_castle_move_num_n(self):
        castle_type = None
        move_num = 10
        assert Move.white_castle_move_num(castle_type, move_num) == 0

    def test_black_castle_move_num_y(self):
        castle_type = "black_short"
        move_num = 10
        assert Move.black_castle_move_num(castle_type, move_num) == 10

    def test_black_castle_move_num_n(self):
        castle_type = None
        move_num = 10
        assert Move.black_castle_move_num(castle_type, move_num) == 0

    def test_get_curr_board(self):
        # Create a MagicMock object to simulate the game_metadata["board"] object
        mock_board = MagicMock(spec=chess.BaseBoard)
        mock_board.board_fen.return_value = (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        )
        self.move_class.game_metadata = {"board": mock_board}

        # Get the current board position
        curr_board = self.move_class.get_curr_board()

        # Assert that the returned board is in the starting position
        self.assertEqual(
            curr_board.board_fen(),
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
        )
        # Assert that the board_fen() method of the mock object was called
        mock_board.board_fen.assert_called_once()

    def test_get_time_spent_on_move(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile.pgn"
        assert (
            self.move_class.get_time_spent_on_move(tempfilepath, 1, (600.0, 600.0, 0))
            == 3.2
        )

    def test_get_time_spent_on_move_interval(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile_timeinterval.pgn"
        assert (
            self.move_class.get_time_spent_on_move(tempfilepath, 1, (600.0, 600.0, 1))
            == 4.2
        )

    def test_filter_timecont_header(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile.pgn"
        assert self.move_class.filter_timecont_header(tempfilepath) == (600.0, 600.0, 0)

    def test_filter_timecont_header_interval(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile_timeinterval.pgn"
        assert self.move_class.filter_timecont_header(tempfilepath) == (600.0, 600.0, 1)

    def test_filter_timecont_header_valueerror(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile_error.pgn"
        assert self.move_class.filter_timecont_header(tempfilepath) == (180.0, 180.0, 0)

    def test_append_to_game_lists(self):
        self.move_class.game_metadata = {
            "game_lists_dict": {
                "gm_mv_num": [],
                "gm_mv": [],
                "gm_best_mv": [],
                "best_move_eval": [],
                "mainline_eval": [],
                "move_eval_diff": [],
                "gm_mv_ac": [],
                "move_type_list": [],
                "w_castle_num": [],
                "b_castle_num": [],
            }
        }
        self.move_class.move_metadata = {"move_num": 1}
        self.move_class.str_ml = "e4"
        self.move_class.str_bm = "e5"
        self.move_class.eval_bm = 0.1
        self.move_class.eval_ml = 0.2
        self.move_class.evaldiff = 0.1
        self.move_class.move_acc = 0.5
        self.move_class.move_type = "normal"
        self.move_class.w_castle_mv_num = 0
        self.move_class.b_castle_mv_num = 0

        # call the method under test
        self.move_class.append_to_game_lists()

        # assert that the game_lists_dict has the expected data
        expected_game_lists_dict = {
            "gm_mv_num": [1],
            "gm_mv": ["e4"],
            "gm_best_mv": ["e5"],
            "best_move_eval": [0.1],
            "mainline_eval": [0.2],
            "move_eval_diff": [0.1],
            "gm_mv_ac": [0.5],
            "move_type_list": ["normal"],
            "w_castle_num": [0],
            "b_castle_num": [0],
        }
        self.assertDictEqual(
            self.move_class.game_metadata["game_lists_dict"], expected_game_lists_dict
        )

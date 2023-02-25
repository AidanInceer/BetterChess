import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import chess.pgn
import pandas as pd

from betterchess.core.game import Game, Prepare
from betterchess.utils.progress import Progress


class TestGame(unittest.TestCase):
    def setUp(self):
        self.input_handler = MagicMock()
        self.input_handler.start_date = 1
        self.input_handler.username = "Ainceer"
        self.input_handler.edepth = 1
        self.file_handler = MagicMock()
        self.run_handler = MagicMock()
        self.env_handler = MagicMock()
        self.iter_metadata = MagicMock()
        self.iter_metadata.return_value = {"game_num": 1, "tot_games": 2}
        self.game = Game(
            self.input_handler,
            self.file_handler,
            self.run_handler,
            self.env_handler,
            self.iter_metadata,
        )
        self.prepare = Prepare()
        self.progress = Progress()
        self.chess_game = MagicMock()
        self.chess_game.mainline_moves.return_value = [1, 2, 3]
        self.move_type_list = [2, 1, 0, -1]
        self.total_moves = 4
        self.game.game_metadata = {
            "game_datetime": 1,
            "game_lists_dict": {
                "gm_mv_ac": [1, 2, 3, 4],
                "w_castle_num": 3,
                "b_castle_num": 4,
            },
            "headers": "headers",
        }
        self.move_dict = {
            "Num_w_best": 1,
            "Num_w_excl": 1,
            "Num_w_good": 1,
            "Num_w_inac": 1,
            "Num_w_mist": 0,
            "Num_w_blun": 0,
            "Num_w_misw": 0,
            "Num_b_best": 1,
            "Num_b_excl": 1,
            "Num_b_good": 1,
            "Num_b_inac": 1,
            "Num_b_mist": 1,
            "Num_b_blun": 1,
            "Num_b_misw": 1,
        }
        self.game_datetime = "10/10/2020"
        self.game_move_acc = [1, 2, 3, 4]
        self.w_castle_num = 3
        self.b_castle_num = 4
        self.total_moves = 4
        self.header1 = {
            "White_rating": 1000,
            "Black_rating": 1200,
            "White_player": "Ainceer",
            "Time_control": "600",
            "Black_player": "Other",
            "User_Colour": "White",
            "User_rating": 1000,
            "Opponent_rating": 1200,
            "User_winner": True,
            "Opening_name": "London",
            "Opening_class": "E40",
            "Termination": "end",
            "Win_draw_loss": "loss",
        }
        self.header2 = {
            "White_rating": 1000,
            "Black_rating": 1200,
            "White_player": "Other",
            "Time_control": "600",
            "Black_player": "Ainceer",
            "User_Colour": "White",
            "User_rating": 1000,
            "Opponent_rating": 1200,
            "User_winner": True,
            "Opening_name": "London",
            "Opening_class": "E40",
            "Termination": "end",
            "Win_draw_loss": "loss",
        }
        self.game_num = 1

    @patch("betterchess.utils.progress.Progress.bar", return_value="time")
    @patch("betterchess.core.game.Game.analyse_game", return_value="output")
    @patch("betterchess.core.move.Move.analyse", return_value="output")
    @patch(
        "betterchess.core.game.Prepare.current_game_analysis",
        return_value={
            "game_datetime": 2,
            "chess_game": MagicMock(),
            "game_lists_dict": {"move_type_list": [1, 2, 3]},
        },
    )
    @patch("betterchess.core.game.Prepare.all_games", return_value=1)
    def test_run_game_analysis(
        self, mock_ag, mock_cga, mock_a, mock_analyse_game, mock_bar
    ):
        self.game.run_game_analysis()
        mock_ag.assert_called_once()
        mock_cga.assert_called_once()
        # mock_a.assert_called()
        mock_analyse_game.assert_called()
        mock_bar.assert_called()

    @patch("betterchess.core.game.Game.sum_move_types")
    @patch("betterchess.core.game.Game.user_game_data")
    @patch("betterchess.core.game.Game.export_game_data")
    def test_analyse_game(self, mock_egd, mock_ugd, mock_smt):
        self.game.analyse_game(self.move_type_list, self.total_moves, self.env_handler)
        mock_egd.assert_called_once()
        mock_ugd.assert_called_once()
        mock_smt.assert_called_once()

    def test_sum_move_types(self):
        move_type_list = [2, 2, 1, 1, 0, 0, -1, -1, -2, -2, -3, -3, -4, -4]
        move_dict = {
            "Num_w_best": 1,
            "Num_b_best": 1,
            "Num_w_excl": 1,
            "Num_b_excl": 1,
            "Num_w_good": 1,
            "Num_b_good": 1,
            "Num_w_inac": 1,
            "Num_b_inac": 1,
            "Num_w_mist": 1,
            "Num_b_mist": 1,
            "Num_w_blun": 1,
            "Num_b_blun": 1,
            "Num_w_misw": 1,
            "Num_b_misw": 1,
        }
        assert Game.sum_move_types(self, move_type_list) == move_dict

    @patch(
        "betterchess.core.game.Game.create_game_data_df",
        return_value=pd.DataFrame({"a": [1, 2], "b": [1, 2]}),
    )
    @patch("betterchess.core.game.Game.collect_white_player_data", return_value=1)
    @patch("betterchess.core.game.Game.get_curr_game_pgn", return_value=1)
    @patch("betterchess.core.game.Game.game_day_of_week", return_value=1)
    @patch("betterchess.core.game.Game.game_time_of_day", return_value=1)
    def test_user_game_data_white(
        self,
        gtod,
        gdow,
        gcgp,
        cwpd,
        cgdd,
    ):
        cwpd.return_value = MagicMock()
        self.game.user_game_data(
            self.move_dict,
            self.game_datetime,
            self.game_move_acc,
            self.w_castle_num,
            self.b_castle_num,
            self.total_moves,
            self.header1,
            self.input_handler.username,
            self.input_handler.edepth,
            self.game_num,
        )
        gtod.assert_called()
        gdow.assert_called()
        gcgp.assert_called()
        cwpd.assert_called()
        cgdd.assert_called()

    @patch(
        "betterchess.core.game.Game.create_game_data_df",
        return_value=pd.DataFrame({"a": [1, 2], "b": [1, 2]}),
    )
    @patch("betterchess.core.game.Game.collect_black_player_data", return_value=1)
    @patch("betterchess.core.game.Game.get_curr_game_pgn", return_value=1)
    @patch("betterchess.core.game.Game.game_day_of_week", return_value=1)
    @patch("betterchess.core.game.Game.game_time_of_day", return_value=1)
    def test_user_game_data_black(
        self,
        gtod,
        gdow,
        gcgp,
        cbpd,
        cgdd,
    ):
        self.game.user_game_data(
            self.move_dict,
            self.game_datetime,
            self.game_move_acc,
            self.w_castle_num,
            self.b_castle_num,
            self.total_moves,
            self.header2,
            self.input_handler.username,
            self.input_handler.edepth,
            self.game_num,
        )
        gtod.assert_called()
        gdow.assert_called()
        gcgp.assert_called()
        cbpd.assert_called()
        cgdd.assert_called()

    def test_game_time_of_day_night(self):
        game_datetime = datetime(2022, 5, 29, 4, 35, 47)
        assert Game.game_time_of_day(game_datetime) == "Night"

    def test_game_time_of_day_morning(self):
        game_datetime = datetime(2022, 5, 29, 9, 35, 47)
        assert Game.game_time_of_day(game_datetime) == "Morning"

    def test_game_time_of_day_afternoon(self):
        game_datetime = datetime(2022, 5, 29, 13, 35, 47)
        assert Game.game_time_of_day(game_datetime) == "Afternoon"

    def test_game_time_of_day_evening(self):
        game_datetime = datetime(2022, 5, 29, 19, 35, 47)
        assert Game.game_time_of_day(game_datetime) == "Evening"

    def test_game_day_of_week(self):
        game_datetime = datetime(2022, 5, 29, 19, 35, 47)
        assert Game.game_day_of_week(game_datetime) == "Sunday"

    def test_game_w_acc(self):
        game_move_acc = [90, 80, 90, 80, 90, 80]
        assert Game.game_w_acc(game_move_acc) == 90

    def test_game_w_acc_zero(self):
        game_move_acc = []
        assert Game.game_w_acc(game_move_acc) == 0

    def test_game_b_acc(self):
        game_move_acc = [90, 80, 90, 80, 90, 80]
        assert Game.game_b_acc(game_move_acc) == 80

    def test_game_b_acc_zero(self):
        game_move_acc = []
        assert Game.game_b_acc(game_move_acc) == 0

    def test_op_w_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert Game.op_w_acc(game_move_acc) == 90

    def test_op_w_acc_zero(self):
        game_move_acc = []
        assert Game.op_w_acc(game_move_acc) == 0

    def test_mid_w_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert Game.mid_w_acc(game_move_acc) == 30

    def test_mid_w_acc_zero(self):
        game_move_acc = []
        assert Game.mid_w_acc(game_move_acc) == 0

    def test_end_w_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert Game.end_w_acc(game_move_acc) == 70

    def test_end_w_acc_zero(self):
        game_move_acc = []
        assert Game.end_w_acc(game_move_acc) == 0

    def test_op_b_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert Game.op_b_acc(game_move_acc) == 80

    def test_op_b_acc_zero(self):
        game_move_acc = []
        assert Game.op_b_acc(game_move_acc) == 0

    def test_mid_b_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert Game.mid_b_acc(game_move_acc) == 20

    def test_mid_b_acc_zero(self):
        game_move_acc = []
        assert Game.mid_b_acc(game_move_acc) == 0

    def test_end_b_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert Game.end_b_acc(game_move_acc) == 60

    def test_end_b_acc_zero(self):
        game_move_acc = []
        assert Game.end_b_acc(game_move_acc) == 0

    def test_w_sec_imp_opening(self):
        ow, mw, ew = 80.0, 90.0, 90.0
        assert Game.w_sec_imp(ow, mw, ew) == "Opening"

    def test_w_sec_imp_midgame(self):
        ow, mw, ew = 90.0, 80.0, 90.0
        assert Game.w_sec_imp(ow, mw, ew) == "Midgame"

    def test_w_sec_imp_endgame(self):
        ow, mw, ew = 90.0, 90.0, 80.0
        assert Game.w_sec_imp(ow, mw, ew) == "Endgame"

    def test_b_sec_imp_opening(self):
        ob, mb, eb = 80.0, 90.0, 90.0
        assert Game.b_sec_imp(ob, mb, eb) == "Opening"

    def test_b_sec_imp_midgame(self):
        ob, mb, eb = 90.0, 80.0, 90.0
        assert Game.b_sec_imp(ob, mb, eb) == "Midgame"

    def test_b_sec_imp_endgame(self):
        ob, mb, eb = 90.0, 90.0, 80.0
        assert Game.b_sec_imp(ob, mb, eb) == "Endgame"

    def test_white_castle_move_num(self):
        white_castle_num = [0, 0, 0, 15]
        assert Game.white_castle_move_num(white_castle_num) == 15

    def test_black_castle_move_num(self):
        black_castle_num = [0, 0, 0, 31]
        assert Game.black_castle_move_num(black_castle_num) == 31

    def test_has_white_castled_yes(self):
        white_castle_num = [0, 0, 0, 1]
        assert Game.has_white_castled(white_castle_num) == 1

    def test_has_white_castled_no(self):
        white_castle_num = [0, 0, 0, 0]
        assert Game.has_white_castled(white_castle_num) == 0

    def test_has_black_castled_yes(self):
        black_castle_num = [0, 0, 0, 2]
        assert Game.has_black_castled(black_castle_num) == 1

    def test_has_black_castled_no(self):
        black_castle_num = [0, 0, 0, 0]
        assert Game.has_black_castled(black_castle_num) == 0

    def test_white_castle_phase_opening(self):
        white_castle_num = [0, 1]
        total_moves = 10
        assert Game.white_castle_phase(white_castle_num, total_moves) == "Opening"

    def test_white_castle_phase_midgame(self):
        white_castle_num = [0, 0, 0, 0, 5]
        total_moves = 10
        assert Game.white_castle_phase(white_castle_num, total_moves) == "Midgame"

    def test_white_castle_phase_endgame(self):
        white_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 9]
        total_moves = 10
        assert Game.white_castle_phase(white_castle_num, total_moves) == "Endgame"

    def test_white_castle_phase_none(self):
        white_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        total_moves = 10
        assert Game.white_castle_phase(white_castle_num, total_moves) == "None"

    def test_white_castle_phase_totnone(self):
        white_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        total_moves = 0
        assert Game.white_castle_phase(white_castle_num, total_moves) == "None"

    def test_black_castle_phase_opening(self):
        black_castle_num = [0, 1]
        total_moves = 10
        assert Game.black_castle_phase(black_castle_num, total_moves) == "Opening"

    def test_black_castle_phase_midgame(self):
        black_castle_num = [0, 0, 0, 0, 5]
        total_moves = 10
        assert Game.black_castle_phase(black_castle_num, total_moves) == "Midgame"

    def test_black_castle_phase_endgame(self):
        black_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 9]
        total_moves = 10
        assert Game.black_castle_phase(black_castle_num, total_moves) == "Endgame"

    def test_black_castle_phase_none(self):
        black_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        total_moves = 10
        assert Game.black_castle_phase(black_castle_num, total_moves) == "None"

    def test_black_castle_phase_totnone(self):
        black_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        total_moves = 0
        assert Game.black_castle_phase(black_castle_num, total_moves) == "None"

    def test_get_predicted_win_percentage(self):
        p1 = 400
        p2 = 400
        assert Game.get_predicted_win_percentage(p1, p2) == 50.0

    def test_get_curr_game_pgn(self):
        path_temp = r"./tests/test_core/fixtures/test_game.pgn"
        assert Game.get_curr_game_pgn(path_temp) == "['chess game']"


class TestPrepare(unittest.TestCase):
    def setUp(self):
        self.prepare = Prepare()
        self.input_handler = MagicMock()
        self.input_handler.start_date = 1
        self.input_handler.username = "Ainceer"
        self.input_handler.edepth = 1
        self.file_handler = MagicMock()
        self.file_handler.path_temp = "./temp"
        self.run_handler = MagicMock()
        self.env_handler = MagicMock()
        self.iter_metadata = MagicMock()
        self.iter_metadata.return_value = {"game_num": 1, "tot_games": 2}

    def test_logfile_line_checker_multi_empty_input(self):
        game_log_list = []
        lines = []
        Prepare.logfile_line_checker_multi(self, game_log_list, lines)
        self.assertEqual(game_log_list, [])

    def test_logfile_line_checker_multi(self):
        game_log_list = []
        lines = ["user", "game", "other"]
        Prepare.logfile_line_checker_multi(self, game_log_list, lines)
        self.assertEqual("user" in game_log_list, True)
        self.assertEqual("game" in game_log_list, True)
        self.assertEqual("other" in game_log_list, False)

    @patch(
        "betterchess.core.headers.Headers.collect",
        return_value={"Game_datetime": "10-10-2020"},
    )
    @patch("betterchess.core.game.Prepare.init_game_lists", return_value=[1, 2, 3, 4])
    @patch("betterchess.core.game.Prepare.init_board", return_value="board")
    @patch("betterchess.core.game.Prepare.init_game", return_value="chess_game")
    def test_current_game_analysis(self, mock_ig, mock_ib, mock_igl, mock_col):
        self.prepare.current_game_analysis(
            self.input_handler, self.file_handler, self.run_handler, self.iter_metadata
        )
        mock_ig.assert_called()
        mock_ib.assert_called()
        mock_igl.assert_called()
        mock_col.assert_called()
        assert self.prepare.current_game_analysis(
            self.input_handler, self.file_handler, self.run_handler, self.iter_metadata
        ) == {
            "headers": {"Game_datetime": "10-10-2020"},
            "game_datetime": "10-10-2020",
            "board": "board",
            "chess_game": "chess_game",
            "game_lists_dict": [1, 2, 3, 4],
        }

    def test_init_game(self):
        path_temp = r"./tests/test_core/fixtures/testpgnfile.pgn"
        chess_game_pgn = open(path_temp)
        expected = chess.pgn.read_game(chess_game_pgn)
        ob1 = isinstance(expected, chess.Board)
        ob2 = isinstance(self.prepare.init_game(path_temp), chess.Board)
        assert ob1 == ob2

    def test_init_board(self):
        path_temp = r"./tests/test_core/fixtures/testpgnfile.pgn"
        chess_game_pgn = open(path_temp)
        chess_game = chess.pgn.read_game(chess_game_pgn)
        assert self.prepare.init_board(chess_game) == chess_game.board()

    def test_init_game_lists(self):
        expected = {
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
        assert self.prepare.init_game_lists() == expected

    @patch("betterchess.core.game.Prepare.get_last_logged_game", return_value=3)
    def test_all_games(self, mock_gllg):
        path = "temp"
        self.prepare.all_games(path)
        mock_gllg.assert_called()
        assert self.prepare.all_games(path) == 3

    @patch(
        "betterchess.core.game.Prepare.get_game_log_list",
        return_value=[
            "[INFO game] | Ainceer | 2020-11-09 16:02:24 | 5",
            "[INFO game] | Ainceer | 2020-11-09 16:27:24 | 6",
        ],
    )
    def test_get_last_logged_game_num(self, mock_loglist):
        path = "test"
        self.prepare.get_last_logged_game(path)
        mock_loglist.assert_called_once()
        assert self.prepare.get_last_logged_game(path) == datetime(
            2020, 11, 9, 16, 27, 24
        )

    def test_game_get_game_log_list(self):
        path_userlogfile = r"./tests/test_core/fixtures/test_log_list.txt"

        assert self.prepare.get_game_log_list(path_userlogfile) == [
            "[INFO user] | Ainceer | 2020-01-01 00:00:00 | 0\n",
            "[INFO game] | Ainceer | 2020-11-08 22:00:49 | 0\n",
            "[INFO game] | Ainceer | 2020-11-08 23:10:17 | 1",
        ]

    def test_game_logfile_line_checker_multi(self):
        game_log_list = []
        lines = ["user", "user_analysis", "false"]
        self.prepare.logfile_line_checker_multi(game_log_list, lines)
        assert game_log_list == ["user", "user_analysis"]

import unittest
from datetime import datetime
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from betterchess.core.game import Game, Prepare


class TestGame(unittest.TestCase):
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

    # @patch("src.user_analysis.ChessGame.game_time_of_day")
    # @patch("src.user_analysis.ChessGame.game_day_of_week")
    # @patch("src.user_analysis.ChessGame.game_w_acc")
    # @patch("src.user_analysis.ChessGame.op_w_acc")
    # @patch("src.user_analysis.ChessGame.mid_w_acc")
    # @patch("src.user_analysis.ChessGame.end_w_acc")
    # @patch("src.user_analysis.ChessGame.w_sec_imp")
    # @patch("src.user_analysis.ChessGame.white_castle_move_num")
    # @patch("src.user_analysis.ChessGame.black_castle_move_num")
    # @patch("src.user_analysis.ChessGame.has_white_castled")
    # @patch("src.user_analysis.ChessGame.has_black_castled")
    # @patch("src.user_analysis.ChessGame.white_castle_phase")
    # @patch("src.user_analysis.ChessGame.black_castle_phase")
    # def test_user_game_data_white(
    #     self,
    #     bcp,
    #     wcp,
    #     hbc,
    #     hwc,
    #     bcmn,
    #     wcmn,
    #     wsi,
    #     eow,
    #     mow,
    #     owa,
    #     gwa,
    #     mock_gdow,
    #     mock_gtod,
    # ):
    #     mock_gtod.return_value = "Afternoon"
    #     mock_gdow.return_value = "Monday"
    #     gwa.return_value = 90
    #     owa.return_value = 90
    #     mow.return_value = 90
    #     eow.return_value = 90
    #     wsi.return_value = "Opening"
    #     wcmn.return_value = 25
    #     bcmn.return_value = 26
    #     hwc.return_value = 1
    #     hbc.return_value = 1
    #     wcp.return_value = "Midgame"
    #     bcp.return_value = "Midgame"
    #     move_dict = {
    #         "Num_w_best": 0,
    #         "Num_b_best": 0,
    #         "Num_w_excl": 35,
    #         "Num_b_excl": 0,
    #         "Num_w_good": 0,
    #         "Num_b_good": 34,
    #         "Num_w_inac": 0,
    #         "Num_b_inac": 0,
    #         "Num_w_mist": 0,
    #         "Num_b_mist": 0,
    #         "Num_w_blun": 0,
    #         "Num_b_blun": 0,
    #         "Num_w_misw": 0,
    #         "Num_b_misw": 0,
    #     }
    #     game_date_time = "2021.02.22 19:35:47"
    #     game_dt = datetime.strptime(game_date_time, "%Y.%m.%d %H:%M:%S")
    #     init_move_acc_list = list(zip([90 for _ in range(34)], [80 for _ in range(34)]))
    #     game_move_acc = [item for sublist in init_move_acc_list for item in sublist] + [
    #         90
    #     ]
    #     w_castle_num = 25
    #     b_castle_num = 26
    #     total_moves = 69
    #     headers = {
    #         "Game_date": "2021.02.22",
    #         "Game_time": "19:35:47",
    #         "Game_datetime": game_dt,
    #         "Time_control": 600,
    #         "Username": "LucidKoala",
    #         "User_Colour": "Black",
    #         "User_rating": 1011,
    #         "Opponent_rating": 1009,
    #         "User_winner": "Win",
    #         "White_player": "JezzaShaw",
    #         "Black_player": "LucidKoala",
    #         "White_rating": 1011,
    #         "Black_rating": 1009,
    #         "Opening_class": "A40",
    #         "Opening_name": "Queens Pawn Opening Mikenas Defense 2.c4 e5 3.d5",
    #         "Termination": "Win by resignation",
    #         "Win_draw_loss": "White",
    #     }
    #     username = "JezzaShaw"
    #     edepth = 1
    #     game_num = 1
    #     test_df = pd.DataFrame(
    #         {
    #             "Username": "JezzaShaw",
    #             "Date": datetime.strptime(game_date_time, "%Y.%m.%d %H:%M:%S"),
    #             "Game_time_of_day": "Afternoon",
    #             "Game_weekday": "Monday",
    #             "Engine_depth": 1,
    #             "Game_number": 1,
    #             "Game_type": 600,
    #             "White_player": "JezzaShaw",
    #             "Black_player": "LucidKoala",
    #             "White_rating": 1011,
    #             "Black_rating": 1009,
    #             "User_colour": "Black",
    #             "User_rating": 1011,
    #             "opponent_rating": 1009,
    #             "User_winner": "Win",
    #             "Opening_name": "Queens Pawn Opening Mikenas Defense 2.c4 e5 3.d5",
    #             "Opening_class": "A40",
    #             "Termination": "Win by resignation",
    #             "End_type": "White",
    #             "Number_of_moves": total_moves,
    #             "Accuracy": 90,
    #             "Opening_accuracy": 90,
    #             "Mid_accuracy": 90,
    #             "End_accuracy": 90,
    #             "No_best": 0,
    #             "No_excellent": 35,
    #             "No_good": 0,
    #             "No_inaccuracy": 0,
    #             "No_mistake": 0,
    #             "No_blunder": 0,
    #             "No_missed_win": 0,
    #             "Improvement": "Opening",
    #             "user_castle_num": 25,
    #             "opp_castle_num": 26,
    #             "user_castled": 1,
    #             "opp_castled": 1,
    #             "user_castle_phase": "Midgame",
    #             "Opp_castle_phase": "Midgame",
    #         },
    #         index=[0],
    #     )
    #     c_game = Game("JezzaShaw", "1", datetime(2020, 1, 1, 1, 1, 1), "", 1, "", "100")
    #     assert_frame_equal(
    #         c_game.user_game_data(
    #             move_dict,
    #             game_dt,
    #             game_move_acc,
    #             w_castle_num,
    #             b_castle_num,
    #             69,
    #             headers,
    #             username,
    #             edepth,
    #             game_num,
    #         ),
    #         test_df,
    #     )

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


class TestPrepare(unittest.TestCase):
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

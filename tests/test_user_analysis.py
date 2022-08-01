import chess
import chess.engine
import pandas as pd
import unittest
from chess import WHITE
from chess.engine import PovScore, Cp, Mate
from datetime import datetime
from pandas.testing import assert_frame_equal
from src.user_analysis import ChessGame
from src.user_analysis import ChessUser
from src.user_analysis import ChessMove
from src.user_analysis import ChessGameHeaders
from src.user_analysis import InputHandler
from unittest.mock import patch
from unittest import TestCase
from logging import Logger


class TestUser(TestCase):
    def test_create_logger(self):
        c_user = ChessUser("Ainceer", 1, datetime(2020, 11, 8, 23, 10, 17))
        c_user.file_paths = BaseFileHandler()
        self.assertIsInstance(c_user.create_logger(), Logger)

    # def test_create_engine(self):
    #     c_user = ChessUser("Ainceer", 1, datetime(2020, 11, 8, 23, 10, 17))
    #     c_user.file_paths = BaseFileHandler()
    #     self.assertIsInstance(c_user.create_engine(), chess.engine.SimpleEngine)

    @patch("src.user_analysis.extract.data_extract")
    @patch("src.user_analysis.ChessUser.analyse_user")
    def test_run_analysis(self, mock_de, mock_au):
        c_user = ChessUser("Ainceer", 1, datetime(2020, 11, 8, 23, 10, 17))
        c_user.logger = "test_logger"
        assert c_user.run_analysis() is None

    # @patch("src.user_analysis.filter.init_all_games")
    # @patch("src.user_analysis.filter.init_game_logs")
    # @patch("src.user_analysis.filter.clean_sql_table")
    # @patch("src.user_analysis.ChessGame.run_game_analysis")
    # @patch("src.user_analysis.ChessUser.write_temp_pgn")
    # @patch("src.user_analysis.filter.get_last_logged_game_num")
    # def test_analyse_user(self, mock_iag, mock_igl, mock_cm, mock_rga, mock_wtp, mock_gllgm):
    #     c_user = ChessUser("Ainceer", 1, datetime(2020, 11, 8, 23, 10, 17))
    #     c_user.file_paths = BaseFileHandler()
    #     c_user.file_paths.temp = BaseFileHandler().temp
    #     c_user.logger = "test_logger"
    #     c_user.engine = "test_engine"
    #     c_user.last_logged_game_num = 1
    #     assert c_user.analyse_user() is None

    # def test_write_temp_pgn(self):
    #     temp_game = "A ; B"
    #     tempfilepath = BaseFileHandler().write_temp
    #     c_user = ChessUser("Ainceer", 1, datetime(2020, 11, 8, 23, 10, 17))
    #     assert c_user.write_temp_pgn(tempfilepath, temp_game) is None


class TestGame(TestCase):
    # @patch("src.user_analysis.ChessGame.init_game_analysis")
    # @patch("src.user_analysis.ChessMove.analyse_move")
    # @patch("src.user_analysis.ChessGame.analyse_game")
    # @patch("src.user_analysis.progress.progress_bar")
    # def test_run_game_analysis_unbounderror(self, mock_iga, mock_am, mock_ag, mock_pb):
    #     logfilepath = BaseFileHandler().logpath
    #     tempfilepath = BaseFileHandler().false_game
    #     enginepath = BaseFileHandler().enginepath
    #     engine = chess.engine.SimpleEngine.popen_uci(enginepath)
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)

    #     logging.basicConfig(
    #         filename=logfilepath,
    #         format="[%(levelname)s %(module)s] %(message)s",
    #         level=logging.INFO,
    #         datefmt="%Y/%m/%d %I:%M:%S",
    #     )
    #     logger = logging.getLogger(__name__)
    #     c_game = ChessGame(
    #         "LucidKoala", "1", datetime(2020, 1, 1, 1, 1, 1), engine, 1, logger, 100
    #     )
    #     c_game.chess_game = chess_game
    #     c_game.board = chess_game.board()
    #     c_game.game_dt = datetime(2020, 11, 8, 23, 10, 17)
    #     c_game.log_dt = datetime(2020, 10, 8, 23, 10, 17)
    #     c_game.gm_mv_num = []
    #     c_game.gm_mv = []
    #     c_game.gm_best_mv = []
    #     c_game.best_move_eval = []
    #     c_game.mainline_eval = []
    #     c_game.move_eval_diff = []
    #     c_game.gm_mv_ac = []
    #     c_game.move_type_list = []
    #     c_game.w_castle_num = []
    #     c_game.b_castle_num = []
    #     assert c_game.run_game_analysis() is None

    # @patch("src.user_analysis.ChessGame.init_game_analysis")
    # @patch("src.user_analysis.ChessMove.analyse_move")
    # @patch("src.user_analysis.ChessGame.analyse_game")
    # @patch("src.user_analysis.progress.progress_bar")
    # def test_run_game_analysis(self, mock_iga, mock_am, mock_ag, mock_pb):
    #     logfilepath = BaseFileHandler().logpath
    #     tempfilepath = BaseFileHandler().test
    #     enginepath = BaseFileHandler().enginepath
    #     engine = chess.engine.SimpleEngine.popen_uci(enginepath)
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)

    #     logging.basicConfig(
    #         filename=logfilepath,
    #         format="[%(levelname)s %(module)s] %(message)s",
    #         level=logging.INFO,
    #         datefmt="%Y/%m/%d %I:%M:%S",
    #     )
    #     logger = logging.getLogger(__name__)
    #     c_game = ChessGame(
    #         "LucidKoala", "1", datetime(2020, 1, 1, 1, 1, 1), engine, 1, logger, 100
    #     )
    #     c_game.chess_game = chess_game
    #     c_game.board = chess_game.board()
    #     c_game.game_dt = datetime(2020, 11, 8, 23, 10, 17)
    #     c_game.log_dt = datetime(2020, 10, 8, 23, 10, 17)
    #     c_game.gm_mv_num = []
    #     c_game.gm_mv = []
    #     c_game.gm_best_mv = []
    #     c_game.best_move_eval = []
    #     c_game.mainline_eval = []
    #     c_game.move_eval_diff = []
    #     c_game.gm_mv_ac = []
    #     c_game.move_type_list = []
    #     c_game.w_castle_num = []
    #     c_game.b_castle_num = []
    #     assert c_game.run_game_analysis() is None

    # @patch("src.user_analysis.ChessGame.init_game")
    # @patch("src.user_analysis.ChessGame.init_board")
    # @patch("src.user_analysis.ChessGame.init_game_lists")
    # @patch("src.user_analysis.ChessGame.game_analysis_filter")
    # def test_init_game_analysis(self, mock_ig, mock_b, mock_igl, mock_gaf):
    #     logfilepath = BaseFileHandler().logpath
    #     tempfilepath = BaseFileHandler().test
    #     enginepath = BaseFileHandler().enginepath
    #     engine = chess.engine.SimpleEngine.popen_uci(enginepath)
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     mock_ig.return_value = chess_game
    #     mock_b.return_value = chess_game.board()
    #     mock_igl.return_value = []
    #     mock_gaf.return_value = "mock_filter"

    #     logging.basicConfig(
    #         filename=logfilepath,
    #         format="[%(levelname)s %(module)s] %(message)s",
    #         level=logging.INFO,
    #         datefmt="%Y/%m/%d %I:%M:%S",
    #     )
    #     logger = logging.getLogger(__name__)
    #     c_game = ChessGame(
    #         "LucidKoala", "1", datetime(2020, 1, 1, 1, 1, 1), engine, 1, logger, 100
    #     )
    #     c_game.chess_game = chess_game
    #     c_game.engine = engine
    #     # headers = {"Game_date": 1, "Game_datetime": datetime(2020, 11, 8, 23, 10, 17)}
    #     assert c_game.init_game_analysis(tempfilepath, chess_game, logfilepath) is None

    @patch("src.user_analysis.ChessGame.sum_move_types", return_value=1)
    @patch("src.user_analysis.ChessGame.user_game_data", return_value=2)
    @patch("src.user_analysis.ChessGame.export_game_data", return_value=3)
    def test_analyse_game(self, mock_smt, mock_usd, mock_egdtc):
        c_game = ChessGame(
            "LucidKoala", "1", datetime(2020, 1, 1, 1, 1, 1), "", 1, "", "100"
        )
        c_game.game_dt = datetime(2020, 11, 8, 23, 10, 17)
        c_game.gm_mv_ac = []
        c_game.w_castle_num = [0]
        c_game.b_castle_num = [0]
        c_game.total_moves = 10
        c_game.headers = {}
        mtl = []
        assert c_game.analyse_game(mtl) is None

    # def test_init_game(self):
    #     tempfilepath = BaseFileHandler().test
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     ob1 = isinstance(chess_game, chess.Board)
    #     ob2 = isinstance(ChessGame.init_game(self, tempfilepath), chess.Board)
    #     assert ob1 == ob2

    # def test_init_board(self):
    #     tempfilepath = BaseFileHandler().test
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     assert ChessGame.init_board(self, chess_game) == chess_game.board()

    def test_init_game_lists(self):
        assert ChessGame.init_game_lists(self) is None

    # def test_game_analysis_filter(self):
    #     tempfilepath = BaseFileHandler().logpath
    #     game_dt = datetime(2020, 11, 8, 23, 10, 17)
    #     assert ChessGame.game_analysis_filter(self, tempfilepath) == game_dt

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
    @patch("src.user_analysis.ChessGame.get_predicted_win_percentage")
    def test_user_game_data_white(
        self,
        gpwp,
        bcp,
        wcp,
        hbc,
        hwc,
        bcmn,
        wcmn,
        wsi,
        eow,
        mow,
        owa,
        gwa,
        mock_gdow,
        mock_gtod,
    ):
        mock_gtod.return_value = "Afternoon"
        mock_gdow.return_value = "Monday"
        gwa.return_value = 90
        owa.return_value = 90
        mow.return_value = 90
        eow.return_value = 90
        wsi.return_value = "Opening"
        wcmn.return_value = 25
        bcmn.return_value = 26
        hwc.return_value = 1
        hbc.return_value = 1
        wcp.return_value = "Midgame"
        bcp.return_value = "Midgame"
        gpwp.return_value = 50.0
        move_dict = {
            "Num_w_best": 0,
            "Num_b_best": 0,
            "Num_w_excl": 35,
            "Num_b_excl": 0,
            "Num_w_good": 0,
            "Num_b_good": 34,
            "Num_w_inac": 0,
            "Num_b_inac": 0,
            "Num_w_mist": 0,
            "Num_b_mist": 0,
            "Num_w_blun": 0,
            "Num_b_blun": 0,
            "Num_w_misw": 0,
            "Num_b_misw": 0,
        }
        game_date_time = "2021.02.22 19:35:47"
        game_dt = datetime.strptime(game_date_time, "%Y.%m.%d %H:%M:%S")
        init_move_acc_list = list(zip([90 for _ in range(34)], [80 for _ in range(34)]))
        game_move_acc = [item for sublist in init_move_acc_list for item in sublist] + [
            90
        ]
        w_castle_num = 25
        b_castle_num = 26
        total_moves = 69
        headers = {
            "Game_date": "2021.02.22",
            "Game_time": "19:35:47",
            "Game_datetime": game_dt,
            "Time_control": 600,
            "Username": "LucidKoala",
            "User_Colour": "Black",
            "User_rating": 1011,
            "Opponent_rating": 1009,
            "User_winner": "Win",
            "White_player": "JezzaShaw",
            "Black_player": "LucidKoala",
            "White_rating": 1011,
            "Black_rating": 1009,
            "Opening_class": "A40",
            "Opening_name": "Queens Pawn Opening Mikenas Defense 2.c4 e5 3.d5",
            "Termination": "Win by resignation",
            "Win_draw_loss": "White",
        }
        username = "JezzaShaw"
        edepth = 1
        game_num = 1
        test_df = pd.DataFrame(
            {
                "Username": "JezzaShaw",
                "Game_date": datetime.strptime(game_date_time, "%Y.%m.%d %H:%M:%S"),
                "Game_time_of_day": "Afternoon",
                "Game_weekday": "Monday",
                "Engine_depth": 1,
                "Game_number": 1,
                "Game_type": 600,
                "White_player": "JezzaShaw",
                "White_rating": 1011,
                "Black_player": "LucidKoala",
                "Black_rating": 1009,
                "User_colour": "Black",
                "User_rating": 1011,
                "Opponent_rating": 1009,
                "User_win_percent": 50.0,
                "Opp_win_percent": 50.0,
                "User_winner": "Win",
                "Opening_name": "Queens Pawn Opening Mikenas Defense 2.c4 e5 3.d5",
                "Opening_class": "A40",
                "Termination": "Win by resignation",
                "End_type": "White",
                "Number_of_moves": total_moves,
                "Accuracy": 90,
                "Opening_accuracy": 90,
                "Mid_accuracy": 90,
                "End_accuracy": 90,
                "No_best": 0,
                "No_excellent": 35,
                "No_good": 0,
                "No_inaccuracy": 0,
                "No_mistake": 0,
                "No_blunder": 0,
                "No_missed_win": 0,
                "Improvement": "Opening",
                "User_castle_num": 25,
                "Opp_castle_num": 26,
                "User_castled": 1,
                "Opp_castled": 1,
                "User_castle_phase": "Midgame",
                "Opp_castle_phase": "Midgame",
            },
            index=[0],
        )
        c_game = ChessGame(
            "JezzaShaw", "1", datetime(2020, 1, 1, 1, 1, 1), "", 1, "", "100"
        )
        assert_frame_equal(
            c_game.user_game_data(
                move_dict,
                game_dt,
                game_move_acc,
                w_castle_num,
                b_castle_num,
                69,
                headers,
                username,
                edepth,
                game_num,
            ),
            test_df,
        )

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
    @patch("src.user_analysis.ChessGame.get_predicted_win_percentage")
    def test_user_game_data_black(
        self,
        gpwp,
        bcp,
        wcp,
        hbc,
        hwc,
        bcmn,
        wcmn,
        wsi,
        eow,
        mow,
        owa,
        gwa,
        mock_gdow,
        mock_gtod,
    ):
        mock_gtod.return_value = "Afternoon"
        mock_gdow.return_value = "Monday"
        gwa.return_value = 90
        owa.return_value = 90
        mow.return_value = 90
        eow.return_value = 90
        wsi.return_value = "Opening"
        wcmn.return_value = 25
        bcmn.return_value = 26
        hwc.return_value = 1
        hbc.return_value = 1
        wcp.return_value = "Midgame"
        bcp.return_value = "Midgame"
        gpwp.return_value = 50.0
        move_dict = {
            "Num_w_best": 0,
            "Num_b_best": 0,
            "Num_w_excl": 35,
            "Num_b_excl": 0,
            "Num_w_good": 0,
            "Num_b_good": 34,
            "Num_w_inac": 0,
            "Num_b_inac": 0,
            "Num_w_mist": 0,
            "Num_b_mist": 0,
            "Num_w_blun": 0,
            "Num_b_blun": 0,
            "Num_w_misw": 0,
            "Num_b_misw": 0,
        }
        game_date_time = "2021.02.22 19:35:47"
        game_dt = datetime.strptime(game_date_time, "%Y.%m.%d %H:%M:%S")
        init_move_acc_list = list(zip([90 for _ in range(34)], [80 for _ in range(34)]))
        game_move_acc = [item for sublist in init_move_acc_list for item in sublist] + [
            90
        ]
        w_castle_num = 25
        b_castle_num = 26
        total_moves = 69
        headers = {
            "Game_date": "2021.02.22",
            "Game_time": "19:35:47",
            "Game_datetime": game_dt,
            "Time_control": 600,
            "Username": "LucidKoala",
            "User_Colour": "Black",
            "User_rating": 1009,
            "Opponent_rating": 1011,
            "User_winner": "Loss",
            "White_player": "JezzaShaw",
            "Black_player": "LucidKoala",
            "White_rating": 1011,
            "Black_rating": 1009,
            "Opening_class": "A40",
            "Opening_name": "Queens Pawn Opening Mikenas Defense 2.c4 e5 3.d5",
            "Termination": "Loss by resignation",
            "Win_draw_loss": "White",
        }
        username = "LucidKoala"
        edepth = 1
        game_num = 1
        test_df = pd.DataFrame(
            {
                "Username": "LucidKoala",
                "Game_date": datetime.strptime(game_date_time, "%Y.%m.%d %H:%M:%S"),
                "Game_time_of_day": "Afternoon",
                "Game_weekday": "Monday",
                "Engine_depth": 1,
                "Game_number": 1,
                "Game_type": 600,
                "White_player": "JezzaShaw",
                "White_rating": 1011,
                "Black_player": "LucidKoala",
                "Black_rating": 1009,
                "User_colour": "Black",
                "User_rating": 1009,
                "Opponent_rating": 1011,
                "User_win_percent": 50.0,
                "Opp_win_percent": 50.0,
                "User_winner": "Loss",
                "Opening_name": "Queens Pawn Opening Mikenas Defense 2.c4 e5 3.d5",
                "Opening_class": "A40",
                "Termination": "Loss by resignation",
                "End_type": "White",
                "Number_of_moves": total_moves,
                "Accuracy": 80.0,
                "Opening_accuracy": 80.0,
                "Mid_accuracy": 80.0,
                "End_accuracy": 80.0,
                "No_best": 0,
                "No_excellent": 0,
                "No_good": 34,
                "No_inaccuracy": 0,
                "No_mistake": 0,
                "No_blunder": 0,
                "No_missed_win": 0,
                "Improvement": "Endgame",
                "User_castle_num": 26,
                "Opp_castle_num": 25,
                "User_castled": 1,
                "Opp_castled": 1,
                "User_castle_phase": "Midgame",
                "Opp_castle_phase": "Midgame",
            },
            index=[0],
        )
        c_game = ChessGame(
            "LucidKoala", "1", datetime(2020, 1, 1, 1, 1, 1), "", 1, "", "100"
        )
        assert_frame_equal(
            c_game.user_game_data(
                move_dict,
                game_dt,
                game_move_acc,
                w_castle_num,
                b_castle_num,
                69,
                headers,
                username,
                edepth,
                game_num,
            ),
            test_df,
        )

    def test_game_time_of_day_night(self):
        game_datetime = datetime(2022, 5, 29, 4, 35, 47)
        assert ChessGame.game_time_of_day(game_datetime) == "Night"

    def test_game_time_of_day_morning(self):
        game_datetime = datetime(2022, 5, 29, 9, 35, 47)
        assert ChessGame.game_time_of_day(game_datetime) == "Morning"

    def test_game_time_of_day_afternoon(self):
        game_datetime = datetime(2022, 5, 29, 13, 35, 47)
        assert ChessGame.game_time_of_day(game_datetime) == "Afternoon"

    def test_game_time_of_day_evening(self):
        game_datetime = datetime(2022, 5, 29, 19, 35, 47)
        assert ChessGame.game_time_of_day(game_datetime) == "Evening"

    def test_game_day_of_week(self):
        game_datetime = datetime(2022, 5, 29, 19, 35, 47)
        assert ChessGame.game_day_of_week(game_datetime) == "Sunday"

    def test_game_w_acc(self):
        game_move_acc = [90, 80, 90, 80, 90, 80]
        assert ChessGame.game_w_acc(game_move_acc) == 90

    def test_game_w_acc_zero(self):
        game_move_acc = []
        assert ChessGame.game_w_acc(game_move_acc) == 0

    def test_game_b_acc(self):
        game_move_acc = [90, 80, 90, 80, 90, 80]
        assert ChessGame.game_b_acc(game_move_acc) == 80

    def test_game_b_acc_zero(self):
        game_move_acc = []
        assert ChessGame.game_b_acc(game_move_acc) == 0

    def test_op_w_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert ChessGame.op_w_acc(game_move_acc) == 90

    def test_op_w_acc_zero(self):
        game_move_acc = []
        assert ChessGame.op_w_acc(game_move_acc) == 0

    def test_mid_w_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert ChessGame.mid_w_acc(game_move_acc) == 30

    def test_mid_w_acc_zero(self):
        game_move_acc = []
        assert ChessGame.mid_w_acc(game_move_acc) == 0

    def test_end_w_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert ChessGame.end_w_acc(game_move_acc) == 70

    def test_end_w_acc_zero(self):
        game_move_acc = []
        assert ChessGame.end_w_acc(game_move_acc) == 0

    def test_op_b_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert ChessGame.op_b_acc(game_move_acc) == 80

    def test_op_b_acc_zero(self):
        game_move_acc = []
        assert ChessGame.op_b_acc(game_move_acc) == 0

    def test_mid_b_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert ChessGame.mid_b_acc(game_move_acc) == 20

    def test_mid_b_acc_zero(self):
        game_move_acc = []
        assert ChessGame.mid_b_acc(game_move_acc) == 0

    def test_end_b_acc(self):
        game_move_acc = [90, 80, 90, 80, 30, 20, 30, 20, 70, 60, 70, 60]
        assert ChessGame.end_b_acc(game_move_acc) == 60

    def test_end_b_acc_zero(self):
        game_move_acc = []
        assert ChessGame.end_b_acc(game_move_acc) == 0

    def test_w_sec_imp_opening(self):
        ow, mw, ew = 80.0, 90.0, 90.0
        assert ChessGame.w_sec_imp(ow, mw, ew) == "Opening"

    def test_w_sec_imp_midgame(self):
        ow, mw, ew = 90.0, 80.0, 90.0
        assert ChessGame.w_sec_imp(ow, mw, ew) == "Midgame"

    def test_w_sec_imp_endgame(self):
        ow, mw, ew = 90.0, 90.0, 80.0
        assert ChessGame.w_sec_imp(ow, mw, ew) == "Endgame"

    def test_b_sec_imp_opening(self):
        ob, mb, eb = 80.0, 90.0, 90.0
        assert ChessGame.b_sec_imp(ob, mb, eb) == "Opening"

    def test_b_sec_imp_midgame(self):
        ob, mb, eb = 90.0, 80.0, 90.0
        assert ChessGame.b_sec_imp(ob, mb, eb) == "Midgame"

    def test_b_sec_imp_endgame(self):
        ob, mb, eb = 90.0, 90.0, 80.0
        assert ChessGame.b_sec_imp(ob, mb, eb) == "Endgame"

    def test_white_castle_move_num(self):
        white_castle_num = [0, 0, 0, 15]
        assert ChessGame.white_castle_move_num(white_castle_num) == 15

    def test_black_castle_move_num(self):
        black_castle_num = [0, 0, 0, 31]
        assert ChessGame.black_castle_move_num(black_castle_num) == 31

    def test_has_white_castled_yes(self):
        white_castle_num = [0, 0, 0, 1]
        assert ChessGame.has_white_castled(white_castle_num) == 1

    def test_has_white_castled_no(self):
        white_castle_num = [0, 0, 0, 0]
        assert ChessGame.has_white_castled(white_castle_num) == 0

    def test_has_black_castled_yes(self):
        black_castle_num = [0, 0, 0, 2]
        assert ChessGame.has_black_castled(black_castle_num) == 1

    def test_has_black_castled_no(self):
        black_castle_num = [0, 0, 0, 0]
        assert ChessGame.has_black_castled(black_castle_num) == 0

    def test_white_castle_phase_opening(self):
        white_castle_num = [0, 1]
        total_moves = 10
        assert ChessGame.white_castle_phase(white_castle_num, total_moves) == "Opening"

    def test_white_castle_phase_midgame(self):
        white_castle_num = [0, 0, 0, 0, 5]
        total_moves = 10
        assert ChessGame.white_castle_phase(white_castle_num, total_moves) == "Midgame"

    def test_white_castle_phase_endgame(self):
        white_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 9]
        total_moves = 10
        assert ChessGame.white_castle_phase(white_castle_num, total_moves) == "Endgame"

    def test_white_castle_phase_none(self):
        white_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        total_moves = 10
        assert ChessGame.white_castle_phase(white_castle_num, total_moves) == "None"

    def test_white_castle_phase_totnone(self):
        white_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        total_moves = 0
        assert ChessGame.white_castle_phase(white_castle_num, total_moves) == "None"

    def test_black_castle_phase_opening(self):
        black_castle_num = [0, 1]
        total_moves = 10
        assert ChessGame.black_castle_phase(black_castle_num, total_moves) == "Opening"

    def test_black_castle_phase_midgame(self):
        black_castle_num = [0, 0, 0, 0, 5]
        total_moves = 10
        assert ChessGame.black_castle_phase(black_castle_num, total_moves) == "Midgame"

    def test_black_castle_phase_endgame(self):
        black_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 9]
        total_moves = 10
        assert ChessGame.black_castle_phase(black_castle_num, total_moves) == "Endgame"

    def test_black_castle_phase_None(self):
        black_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        total_moves = 10
        assert ChessGame.black_castle_phase(black_castle_num, total_moves) == "None"

    def test_black_castle_phase_totNone(self):
        black_castle_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        total_moves = 0
        assert ChessGame.black_castle_phase(black_castle_num, total_moves) == "None"


class TestMove(unittest.TestCase):
    # def test_analyse_move(self):
    #     enginepath = BaseFileHandler().enginepath
    #     engine = chess.engine.SimpleEngine.popen_uci(enginepath)
    #     logger = logging.Logger("test")
    #     tempfilepath = BaseFileHandler().test
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     board = chess_game.board()
    #     move_l_init = chess_game.mainline_moves()
    #     move_l = []
    #     for move in move_l_init:
    #         move_l.append(move)
    #     move = move_l[0]
    #     chessmove = ChessMove(
    #         "LucidKoala",
    #         1,
    #         datetime(2020, 1, 1, 1, 1, 1),
    #         engine,
    #         logger,
    #         100,
    #         chess_game,
    #         1,
    #         board,
    #         0,
    #         "",
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #     )
    #     assert chessmove.analyse_move(move) is None

    # def test_mainline_move(self):
    #     enginepath = BaseFileHandler().enginepath
    #     engine = chess.engine.SimpleEngine.popen_uci(enginepath)
    #     logger = logging.Logger("test")
    #     tempfilepath = BaseFileHandler().test
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     board = chess_game.board()
    #     move_l_init = chess_game.mainline_moves()
    #     move_l = []
    #     for move in move_l_init:
    #         move_l.append(move)
    #     move = move_l[0]
    #     chessmove = ChessMove(
    #         "LucidKoala",
    #         1,
    #         datetime(2020, 1, 1, 1, 1, 1),
    #         engine,
    #         logger,
    #         100,
    #         chess_game,
    #         1,
    #         board,
    #         0,
    #         "",
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #     )
    #     assert chessmove.mainline_move(move, board, engine) == ("d2d4", 31)

    # def test_best_move(self):
    #     enginepath = BaseFileHandler().enginepath
    #     engine = chess.engine.SimpleEngine.popen_uci(enginepath)
    #     logger = logging.Logger("test")
    #     tempfilepath = BaseFileHandler().test
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     board = chess_game.board()
    #     chessmove = ChessMove(
    #         "LucidKoala",
    #         1,
    #         datetime(2020, 1, 1, 1, 1, 1),
    #         engine,
    #         logger,
    #         100,
    #         chess_game,
    #         1,
    #         board,
    #         0,
    #         "",
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #         [],
    #     )
    #     assert chessmove.best_move(board, engine) == ("d2d4", 31)

    def test_move_eval(self):
        move = {"score": PovScore(Cp(10), WHITE)}
        assert 10 == ChessMove.move_eval(move)

    def test_move_eval_mate(self):
        move = {"score": PovScore(Mate(-0), WHITE)}
        assert 0 == ChessMove.move_eval(move)

    def test_eval_delta_white(self):
        move_num, eval_bm, eval_ml = 2, 200, 20
        assert ChessMove.eval_delta(move_num, eval_bm, eval_ml) == 180

    def test_eval_delta_black(self):
        move_num, eval_bm, eval_ml = 3, 20, 20
        assert ChessMove.eval_delta(move_num, eval_bm, eval_ml) == 0

    def test_move_accuracy(self):
        ed = 100
        assert ChessMove.move_accuracy(ed) == 87.5

    def test_assign_move_type_p2(self):
        move_acc = 100
        assert ChessMove.assign_move_type(move_acc) == 2

    def test_assign_move_type_p1(self):
        move_acc = 99.7
        assert ChessMove.assign_move_type(move_acc) == 1

    def test_assign_move_type_p0(self):
        move_acc = 90
        assert ChessMove.assign_move_type(move_acc) == 0

    def test_assign_move_type_n1(self):
        move_acc = 60
        assert ChessMove.assign_move_type(move_acc) == -1

    def test_assign_move_type_n2(self):
        move_acc = 35
        assert ChessMove.assign_move_type(move_acc) == -2

    def test_assign_move_type_n3(self):
        move_acc = 20
        assert ChessMove.assign_move_type(move_acc) == -3

    def test_assign_move_type_n4(self):
        move_acc = 0
        assert ChessMove.assign_move_type(move_acc) == -4

    def test_get_piece_square_int(self):
        move = "a1a2"
        assert ChessMove.get_piece_square_int(move) == 8

    def test_chess_piece_pawn(self):
        curr_board = chess.BaseBoard()
        square_int = 8
        assert "pawn" == ChessMove.chess_piece(curr_board, square_int)

    def test_chess_piece_knight(self):
        curr_board = chess.BaseBoard()
        square_int = 1
        assert "knight" == ChessMove.chess_piece(curr_board, square_int)

    def test_chess_piece_bishop(self):
        curr_board = chess.BaseBoard()
        square_int = 2
        assert "bishop" == ChessMove.chess_piece(curr_board, square_int)

    def test_chess_piece_rook(self):
        curr_board = chess.BaseBoard()
        square_int = 0
        assert "rook" == ChessMove.chess_piece(curr_board, square_int)

    def test_chess_piece_queen(self):
        curr_board = chess.BaseBoard()
        square_int = 3
        assert "queen" == ChessMove.chess_piece(curr_board, square_int)

    def test_chess_piece_king(self):
        curr_board = chess.BaseBoard()
        square_int = 4
        assert "king" == ChessMove.chess_piece(curr_board, square_int)

    def test_chess_piece_none(self):
        curr_board = chess.BaseBoard()
        square_int = 32
        assert " " == ChessMove.chess_piece(curr_board, square_int)

    def test_move_colour_white(self):
        move_num = 2
        assert ChessMove.move_colour(move_num) == "white"

    def test_move_colour_black(self):
        move_num = 3
        assert ChessMove.move_colour(move_num) == "black"

    def test_castling_type_ws(self):
        piece = "king"
        move_col = "white"
        str_ml = "e1g1"
        assert "white_short" == ChessMove.castling_type(piece, move_col, str_ml)

    def test_castling_type_wl(self):
        piece = "king"
        move_col = "white"
        str_ml = "e1c1"
        assert "white_long" == ChessMove.castling_type(piece, move_col, str_ml)

    def test_castling_type_bs(self):
        piece = "king"
        move_col = "black"
        str_ml = "e8g8"
        assert "black_short" == ChessMove.castling_type(piece, move_col, str_ml)

    def test_castling_type_bl(self):
        piece = "king"
        move_col = "black"
        str_ml = "e8c8"
        assert "black_long" == ChessMove.castling_type(piece, move_col, str_ml)

    def test_castling_type_none(self):
        piece = "pawn"
        move_col = "white"
        str_ml = "e1g1"
        assert ChessMove.castling_type(piece, move_col, str_ml) is None

    def test_white_castle_move_num_y(self):
        castle_type = "white_short"
        move_num = 10
        assert ChessMove.white_castle_move_num(castle_type, move_num) == 10

    def test_white_castle_move_num_n(self):
        castle_type = None
        move_num = 10
        assert ChessMove.white_castle_move_num(castle_type, move_num) == 0

    def test_black_castle_move_num_y(self):
        castle_type = "black_short"
        move_num = 10
        assert ChessMove.black_castle_move_num(castle_type, move_num) == 10

    def test_black_castle_move_num_n(self):
        castle_type = None
        move_num = 10
        assert ChessMove.black_castle_move_num(castle_type, move_num) == 0

    # def test_get_time_spent_on_move_white(self) -> float:
    #     self.file_path = BaseFileHandler().test
    #     move_num = 2
    #     timers = (600, 600, 0)
    #     assert 2.7 == ChessMove.get_time_spent_on_move(self.file_path, move_num, timers)

    # def test_get_time_spent_on_move_black(self) -> float:
    #     self.file_path = BaseFileHandler().test
    #     move_num = 3
    #     timers = (600, 600, 0)
    #     assert 5.1 == ChessMove.get_time_spent_on_move(self.file_path, move_num, timers)

    # def test_filter_timecont_header(self):
    #     self.file_path = BaseFileHandler().test
    #     assert ChessMove.filter_timecont_header(self.file_path) == (600, 600, 0)

    # def test_filter_timecont_header_interval(self):
    #     self.file_path = BaseFileHandler().test2
    #     assert ChessMove.filter_timecont_header(self.file_path) == (180, 180, 5)

    def test_create_move_df(self):
        test_move_df = pd.DataFrame(
            {
                "Username": "Ainceer",
                "Game_date": "2020-11-01 00:00:00",
                "Engine_depth": 10,
                "Game_number": 1,
                "Move_number": 1,
                "Move": "e2e4",
                "Move_eval": 1,
                "Best_move": "e2e4",
                "Best_move_eval": 1,
                "Move_eval_diff": 0,
                "Move_accuracy": 100,
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

    # def test_export_move_data(self):
    #     self.file_paths = BaseFileHandler()
    #     self.file_paths.move_data = r"test.csv"
    #     self.username = "Ainceer"

    #     self.test_df = pd.DataFrame({"Username": self.username}, index=[0])
    #     with mock.patch.object(self.test_df, "to_sql") as to_sql_mock:
    #         ChessMove.export_move_data(self, self.file_paths.move_data, self.test_df)
    #         to_sql_mock.assert_called_with(
    #             "test.csv", mode="a", header=False, index=False
    #         )


class TestGameHeaders(unittest.TestCase):
    def test_collect_headers(self):
        pass

    # def test_time_control(self):
    #     tempfilepath = BaseFileHandler().test
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     assert ChessGameHeaders.time_control(self, chess_game) == "600"

    # def test_player_white(self):
    #     tempfilepath = BaseFileHandler().test
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     assert ChessGameHeaders.player_white(self, chess_game) == "JezzaShaw"

    # def test_player_black(self):
    #     tempfilepath = BaseFileHandler().test
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     assert ChessGameHeaders.player_black(self, chess_game) == "LucidKoala"

    def test_user_colour_true(self):
        white = "JezzaShaw"
        username = "JezzaShaw"
        assert ChessGameHeaders.user_colour(self, white, username) == "White"

    def test_user_colour_false(self):
        white = "JezzaShaw"
        username = "LucidKoala"
        assert ChessGameHeaders.user_colour(self, white, username) == "Black"

    # def test_rating_white(self):
    #     tempfilepath = BaseFileHandler().test
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     assert ChessGameHeaders.rating_white(self, chess_game) == 1011

    # def test_test_rating_black(self):
    #     tempfilepath = BaseFileHandler().test
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     assert ChessGameHeaders.rating_black(self, chess_game) == 1009

    # def test_opening_cls_no_err(self):
    #     tempfilepath = BaseFileHandler().test
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     assert ChessGameHeaders.opening_cls(self, chess_game) == "A40"

    # def test_opening_cls_key_err(self):
    #     tempfilepath = BaseFileHandler().test2
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     assert ChessGameHeaders.opening_cls(self, chess_game) == "000"

    # def test_opening_nm(self):
    #     tempfilepath = BaseFileHandler().test
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     assert (
    #         ChessGameHeaders.opening_nm(self, chess_game)
    #         == "Queens Pawn Opening Mikenas Defense 2.c4 e5 3.d5"
    #     )

    # def test_opening_nm_keyerror(self):
    #     tempfilepath = BaseFileHandler().test2
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     assert ChessGameHeaders.opening_nm(self, chess_game) == "NA"

    # def test_game_termination_loss(self):
    #     tempfilepath = BaseFileHandler().test2
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     username = "LucidKoala"
    #     assert (
    #         ChessGameHeaders.game_termination(self, chess_game, username)
    #         == "Loss by resignation"
    #     )

    # def test_game_termination_win(self):
    #     tempfilepath = BaseFileHandler().test2
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     username = "JezzaShaw"
    #     assert (
    #         ChessGameHeaders.game_termination(self, chess_game, username)
    #         == "Win by resignation"
    #     )

    # def test_game_termination_draw(self):
    #     tempfilepath = BaseFileHandler().test_draw
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     username = "LucidKoala"
    #     assert (
    #         ChessGameHeaders.game_termination(self, chess_game, username)
    #         == "Draw by agreement"
    #     )

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

    # def test_win_draw_loss_white(self):
    #     tempfilepath = BaseFileHandler().test
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     assert ChessGameHeaders.win_draw_loss(self, chess_game) == "White"

    # def test_win_draw_loss_black(self):
    #     tempfilepath = BaseFileHandler().test2
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     assert ChessGameHeaders.win_draw_loss(self, chess_game) == "Black"

    # def test_win_draw_loss_draw(self):
    #     tempfilepath = BaseFileHandler().test_draw
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     assert ChessGameHeaders.win_draw_loss(self, chess_game) == "Draw"

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

    # def test_game_dt(self):
    #     tempfilepath = BaseFileHandler().test
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     assert ChessGameHeaders.game_dt(self, chess_game) == "2021.02.22"

    # def test_game_t(self):
    #     tempfilepath = BaseFileHandler().test
    #     chess_game_pgn = open(tempfilepath)
    #     chess_game = read_game(chess_game_pgn)
    #     assert ChessGameHeaders.game_t(self, chess_game) == "19:35:47"

    def test_game_dt_time(self):
        game_date = "2021.02.22"
        game_time = "19:35:47"
        assert ChessGameHeaders.game_dt_time(self, game_date, game_time) == datetime(
            2021, 2, 22, 19, 35, 47
        )


class TestInputHandler(unittest.TestCase):
    @patch("src.user_analysis.InputHandler.user_input", return_value="Ainceer")
    @patch("src.user_analysis.InputHandler.depth_input", return_value=1)
    @patch("src.user_analysis.InputHandler.year_input", return_value=2021)
    @patch("src.user_analysis.InputHandler.month_input", return_value=11)
    @patch("src.user_analysis.InputHandler.start_datetime", return_value="2021-11-01")
    def test_get_inputs(self, mock_ui, mock_di, mock_yi, mock_mi, mock_sd):
        return_dict = {"username": "Ainceer", "edepth": 1, "start_date": "2021-11-01"}
        assert InputHandler.get_inputs() == return_dict

    @patch("builtins.input")
    def test_user_input(self, mock_ui):
        mock_ui.return_value = "Ainceer"
        assert InputHandler.user_input() == "Ainceer"

    @patch("builtins.input")
    def test_depth_input(self, mock_di):
        mock_di.return_value = "1"
        assert InputHandler.depth_input() == "1"

    @patch("builtins.input")
    def test_year_input(self, mock_yi):
        mock_yi.return_value = "2020"
        assert InputHandler.year_input() == "2020"

    @patch("builtins.input")
    def test_month_input(self, mock_mi):
        mock_mi.return_value = "01"
        assert InputHandler.month_input() == "01"

    def test_start_datetime(self):
        start_year = "2020"
        start_month = "01"
        assert InputHandler.start_datetime(start_year, start_month) == datetime(
            2020, 1, 1, 0, 0, 0
        )


class BaseFileHandler:
    def __init__(self):
        self.move_data = r"./test_files/test_move_data.csv"
        self.test = r"tests/test_files/test.pgn"
        self.test2 = r"tests/test_files/test2.pgn"
        self.test_draw = r"tests/test_files/test_draw.pgn"
        self.logpath = r"tests/test_files/test.log"
        self.userlogfile = r"tests/test_files/test_userlog.log"
        self.enginepath = r"./lib/stkfsh_14.1/stk_14.1.exe"
        self.stockfish = r"./lib/stkfsh_14.1/stk_14.1.exe"
        self.pgn_data = r"tests/test_files/test_pgndata.csv"
        self.write_temp = r"tests/test_files/write_temppgn.csv"
        self.temp = r"tests/test_files/temp.pgn"
        self.false_game = r"tests/test_files/false_game.pgn"
        self.db_location = r"tests/test_files/db"

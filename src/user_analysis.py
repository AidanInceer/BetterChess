"""Module for analysing a users games/move data."""
import chess
import chess.engine
import chess.pgn
from chess import Board
import math
import os
import logging
import numpy as np
import pandas as pd
import time
import sqlite3
from src import progress
from src import extract
from src import filter
from datetime import date
from datetime import datetime
from logging import Logger


class ChessUser:
    """Information and methods relating to a user of Chess.com."""

    def __init__(self, username: str, edepth: int, start_date: datetime):
        self.username = username
        self.edepth = edepth
        self.start_date = start_date
        self.file_paths = FileHandler(username=self.username)

    def create_logger(self) -> Logger:
        """Creates a logger for data extract and user game analysis."""
        logging.basicConfig(
            filename=self.file_paths.userlogfile,
            format="[%(levelname)s %(module)s] %(message)s",
            level=logging.INFO,
            datefmt="%Y/%m/%d %I:%M:%S",
        )
        self.logger = logging.getLogger(__name__)
        return self.logger

    def create_engine(self) -> chess.engine.SimpleEngine:
        """Initializes a the chess engine."""
        self.engine = chess.engine.SimpleEngine.popen_uci(self.file_paths.stockfish)
        return self.engine

    def run_analysis(self) -> None:
        """Extracts users data and runs the analysis on their games."""
        extract.data_extract(
            self.username,
            self.file_paths.pgn_data,
            self.file_paths.userlogfile,
            self.logger,
        )
        self.analyse_user()

    def analyse_user(self) -> None:
        """Analyses all of the given users games."""
        all_games = self.init_all_games(self.file_paths.pgn_data)
        print("Analysing users data: ")
        filter.init_game_logs(self.file_paths.userlogfile, self.logger)
        self.last_logged_game_num = filter.get_last_logged_game_num(
            self.file_paths.userlogfile
        )
        filter.clean_sql_table(
            database=self.file_paths.db_location,
            game_num=self.last_logged_game_num,
            username=self.username,
        )
        for game_num, chess_game in enumerate(all_games["game_data"]):
            self.write_temp_pgn(self.file_paths.temp, temp_game=chess_game)
            game = ChessGame(
                self.username,
                self.edepth,
                self.start_date,
                self.engine,
                game_num,
                self.logger,
                self.tot_games,
            )
            game.run_game_analysis()
            del game
        print("\nFinalising analysis")

    def init_all_games(self, filepath) -> pd.DataFrame:
        """Returns a dataframe of all users games from the users pgn csv."""
        all_games = pd.read_csv(
            filepath, delimiter="|", names=["url_date", "game_data"]
        )
        self.tot_games = len(all_games["game_data"])
        return all_games

    def write_temp_pgn(self, tempfilepath, temp_game) -> None:
        """Writes the current game to the temp.pgn file."""
        with open(tempfilepath, "w") as temp_pgn:
            temp_pgn.write(str(temp_game.replace(" ; ", "\n")))


class ChessGame(ChessUser):
    """Chess game for analysis."""

    def __init__(
        self,
        username: str,
        edepth: int,
        start_date: datetime,
        engine: chess.engine.SimpleEngine,
        game_num: int,
        logger: Logger,
        tot_games: int,
    ):
        super().__init__(username, edepth, start_date)
        self.engine = engine
        self.game_num = game_num
        self.logger = logger
        self.tot_games = tot_games

    def run_game_analysis(self) -> None:
        """main function for ChessGame class, runs the init."""
        self.chess_game = self.init_game(self.file_paths.temp)
        self.init_game_analysis(
            self.file_paths.temp, self.chess_game, self.file_paths.userlogfile
        )
        if self.game_dt >= self.log_dt and self.game_dt >= self.start_date:
            start = time.perf_counter()
            self.logger.info(f"| {self.game_dt} |{self.game_num}")
            for move_num, move in enumerate(self.chess_game.mainline_moves()):
                chess_move = ChessMove(
                    self.username,
                    self.edepth,
                    self.start_date,
                    self.engine,
                    self.logger,
                    self.tot_games,
                    self.chess_game,
                    self.game_num,
                    self.board,
                    move_num,
                    self.game_dt,
                    self.gm_mv_num,
                    self.gm_mv,
                    self.gm_best_mv,
                    self.best_move_eval,
                    self.mainline_eval,
                    self.move_eval_diff,
                    self.gm_mv_ac,
                    self.move_type_list,
                    self.w_castle_num,
                    self.b_castle_num,
                )
                chess_move.analyse_move(move)
                del chess_move
            try:
                self.total_moves = move_num
            except UnboundLocalError:
                self.total_moves = 0
            self.analyse_game(self.move_type_list)
            end = time.perf_counter()
            progress.progress_bar(self.game_num, self.tot_games, start, end)

    def init_game_analysis(self, tempfilepath, chess_game, user_logfile) -> None:
        """Initalises the analysis, headers and filters past analysis runs."""
        self.init_board(chess_game)
        self.init_game_lists()
        game_headers = ChessGameHeaders(
            self.username,
            self.edepth,
            self.start_date,
            self.engine,
            self.game_num,
            self.logger,
            self.tot_games,
            chess_game,
        )
        self.headers = game_headers.collect_headers()
        self.game_dt = game_headers.collect_headers()["Game_datetime"]
        self.game_analysis_filter(user_logfile)

    def analyse_game(self, move_type_list) -> None:
        """
        Prepares move data so it can be analysed at a game level
        and exports game data.
        """
        self.sum_type_dict = self.sum_move_types(move_type_list)
        self.game_df = self.user_game_data(
            self.sum_type_dict,
            self.game_dt,
            self.gm_mv_ac,
            self.w_castle_num,
            self.b_castle_num,
            self.total_moves,
            self.headers,
            self.username,
            self.edepth,
            self.game_num,
        )
        self.export_game_data(self.game_df)

    def init_game(self, filepath) -> chess.pgn.Game:
        """Initialises the chess game."""
        chess_game_pgn = open(filepath)
        self.chess_game = chess.pgn.read_game(chess_game_pgn)
        return self.chess_game

    def init_board(self, chess_game) -> chess.Board:
        """Initialises the chess board."""
        self.board = chess_game.board()
        return self.board

    def init_game_lists(self) -> None:
        """Initialises the data lists."""
        self.gm_mv_num = []
        self.gm_mv = []
        self.gm_best_mv = []
        self.best_move_eval = []
        self.mainline_eval = []
        self.move_eval_diff = []
        self.gm_mv_ac = []
        self.move_type_list = []
        self.w_castle_num = []
        self.b_castle_num = []

    def game_analysis_filter(self, logfilepath) -> None:
        """
        Calls the analysis filter module to remove incomplete
        game analysis runs.
        """
        self.log_dt = filter.get_last_logged_game(logfilepath)
        return self.log_dt

    def sum_move_types(self, move_type_list) -> dict:
        """Returns a dictionary of the sum move types for black and white."""
        self.b_best = move_type_list[1::2].count(2)
        self.w_best = move_type_list[::2].count(2)
        self.w_excl = move_type_list[::2].count(1)
        self.w_excl = move_type_list[1::2].count(1)
        self.w_good = move_type_list[::2].count(0)
        self.b_good = move_type_list[1::2].count(0)
        self.w_inac = move_type_list[::2].count(-1)
        self.b_inac = move_type_list[1::2].count(-1)
        self.w_mist = move_type_list[::2].count(-2)
        self.b_mist = move_type_list[1::2].count(-2)
        self.w_blun = move_type_list[::2].count(-3)
        self.b_blun = move_type_list[1::2].count(-3)
        self.w_misw = move_type_list[::2].count(-4)
        self.b_misw = move_type_list[1::2].count(-4)
        self.move_dict = {
            "Num_w_best": self.w_best,
            "Num_b_best": self.b_best,
            "Num_w_excl": self.w_excl,
            "Num_b_excl": self.w_excl,
            "Num_w_good": self.w_good,
            "Num_b_good": self.b_good,
            "Num_w_inac": self.w_inac,
            "Num_b_inac": self.b_inac,
            "Num_w_mist": self.w_mist,
            "Num_b_mist": self.b_mist,
            "Num_w_blun": self.w_blun,
            "Num_b_blun": self.b_blun,
            "Num_w_misw": self.w_misw,
            "Num_b_misw": self.b_misw,
        }
        return self.move_dict

    def user_game_data(
        self,
        move_dict: dict,
        game_dt: str,
        game_move_acc: list,
        w_castle_num: list,
        b_castle_num: list,
        total_moves: int,
        headers: dict,
        username: str,
        edepth: int,
        game_num: int,
    ) -> None:
        """
        Prepares move/game analysis for export and assigns data to
        user/opp depending on what colour the user is playing as.
        """
        self.time_of_day = self.game_time_of_day(game_dt)
        self.day_of_week = self.game_day_of_week(game_dt)
        if username == headers["White_player"]:
            self.game_acc = self.game_w_acc(game_move_acc)
            self.opn_acc = self.op_w_acc(game_move_acc)
            self.mid_acc = self.mid_w_acc(game_move_acc)
            self.end_acc = self.end_w_acc(game_move_acc)
            self.num_best_mv = move_dict["Num_w_best"]
            self.num_excl_mv = move_dict["Num_w_excl"]
            self.num_good_mv = move_dict["Num_w_good"]
            self.num_inac_mv = move_dict["Num_w_inac"]
            self.num_mist_mv = move_dict["Num_w_mist"]
            self.num_blun_mv = move_dict["Num_w_blun"]
            self.num_misw_mv = move_dict["Num_w_misw"]
            self.sec_improve = self.w_sec_imp(self.opn_acc, self.mid_acc, self.end_acc)
            self.user_castle_mv = self.white_castle_move_num(w_castle_num)
            self.opp_castle_mv = self.black_castle_move_num(b_castle_num)
            self.user_castled = self.has_white_castled(w_castle_num)
            self.opp_castled = self.has_black_castled(b_castle_num)
            self.user_castle_phase = self.white_castle_phase(w_castle_num, total_moves)
            self.opp_castle_phase = self.black_castle_phase(b_castle_num, total_moves)
        else:
            self.game_acc = self.game_b_acc(game_move_acc)
            self.opn_acc = self.op_b_acc(game_move_acc)
            self.mid_acc = self.mid_b_acc(game_move_acc)
            self.end_acc = self.end_b_acc(game_move_acc)
            self.num_best_mv = move_dict["Num_b_best"]
            self.num_excl_mv = move_dict["Num_b_excl"]
            self.num_good_mv = move_dict["Num_b_good"]
            self.num_inac_mv = move_dict["Num_b_inac"]
            self.num_mist_mv = move_dict["Num_b_mist"]
            self.num_blun_mv = move_dict["Num_b_blun"]
            self.num_misw_mv = move_dict["Num_b_misw"]
            self.sec_improve = self.b_sec_imp(self.opn_acc, self.mid_acc, self.end_acc)
            self.user_castle_mv = self.black_castle_move_num(b_castle_num)
            self.opp_castle_mv = self.white_castle_move_num(w_castle_num)
            self.user_castled = self.has_black_castled(b_castle_num)
            self.opp_castled = self.has_white_castled(w_castle_num)
            self.user_castle_phase = self.black_castle_phase(w_castle_num, total_moves)
            self.opp_castle_phase = self.white_castle_phase(w_castle_num, total_moves)
        game_df = pd.DataFrame(
            {
                "Username": username,
                "Game_date": game_dt,
                "Game_time_of_day": self.time_of_day,
                "Game_weekday": self.day_of_week,
                "Engine_depth": edepth,
                "Game_number": game_num,
                "Game_type": headers["Time_control"],
                "White_player": headers["White_player"],
                "Black_player": headers["Black_player"],
                "White_rating": headers["White_rating"],
                "Black_rating": headers["Black_rating"],
                "User_colour": headers["User_Colour"],
                "User_rating": headers["User_rating"],
                "Opponent_rating": headers["Opponent_rating"],
                "User_winner": headers["User_winner"],
                "Opening_name": headers["Opening_name"],
                "Opening_class": headers["Opening_class"],
                "Termination": headers["Termination"],
                "End_type": headers["Win_draw_loss"],
                "Number_of_moves": total_moves,
                "Accuracy": self.game_acc,
                "Opening_accuracy": self.opn_acc,
                "Mid_accuracy": self.mid_acc,
                "End_accuracy": self.end_acc,
                "No_best": self.num_best_mv,
                "No_excellent": self.num_excl_mv,
                "No_good": self.num_good_mv,
                "No_inaccuracy": self.num_inac_mv,
                "No_mistake": self.num_mist_mv,
                "No_blunder": self.num_blun_mv,
                "No_missed_win": self.num_misw_mv,
                "Improvement": self.sec_improve,
                "User_castle_num": self.user_castle_mv,
                "Opp_castle_num": self.opp_castle_mv,
                "User_castled": self.user_castled,
                "Opp_castled": self.opp_castled,
                "User_castle_phase": self.user_castle_phase,
                "Opp_castle_phase": self.opp_castle_phase,
            },
            index=[0],
        )
        return game_df

    def export_game_data(self, game_df: pd.DataFrame):
        """Exports game data to csv.

        Args:
            game_df (pd.Dataframe): dataframe of game data
        """
        conn = sqlite3.connect(FileHandler(username=self.username).db_location)
        game_df.to_sql("game_data", conn, if_exists="append", index=False)
        conn.commit
        conn.close

    @staticmethod
    def game_time_of_day(game_datetime) -> str:
        """Returns the time of day as a string"""
        day_hour = int(date.strftime(game_datetime, "%H"))
        if day_hour <= 6:
            time_of_day = "Night"
        elif day_hour <= 12:
            time_of_day = "Morning"
        elif day_hour <= 18:
            time_of_day = "Afternoon"
        elif day_hour <= 24:
            time_of_day = "Evening"
        return time_of_day

    @staticmethod
    def game_day_of_week(game_datetime) -> str:
        """Returns the day of the week that the game is played."""
        week_num_base = int(date.isoweekday(game_datetime))
        weekday_num = week_num_base - 1
        weekdays = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        return weekdays[weekday_num]

    @staticmethod
    def game_w_acc(game_move_acc: list) -> float:
        """Returns white players game accuracy."""
        w_list = game_move_acc[::2]
        list_len = len(game_move_acc[::2])
        if list_len == 0:
            wg_acc = 0
        else:
            wg_acc = round(sum(w_list) / list_len, 2)
        return wg_acc

    @staticmethod
    def game_b_acc(game_move_acc: list) -> float:
        """Returns black players game for accuracy."""
        b__list = game_move_acc[1::2]
        list_len = len(game_move_acc[1::2])
        if list_len == 0:
            bg_acc = 0
        else:
            bg_acc = round(sum(b__list) / list_len, 2)
        return bg_acc

    @staticmethod
    def op_w_acc(game_move_acc: list) -> float:
        """Calculates the opening accuracy for white."""
        list_w = game_move_acc[::2]
        op_list_w = np.array_split(list_w, 3)[0]
        sep_len = len(op_list_w)
        if sep_len == 0:
            white_opening_acc = 0
        else:
            white_opening_acc = round(sum(op_list_w) / (sep_len), 2)
        return white_opening_acc

    @staticmethod
    def mid_w_acc(game_move_acc: list) -> float:
        """Calculates the midgame accuracy for white."""
        list_w = game_move_acc[::2]
        mid_list_w = np.array_split(list_w, 3)[1]
        sep_len = len(mid_list_w)
        if sep_len == 0:
            white_midgame_acc = 0
        else:
            white_midgame_acc = round(sum(mid_list_w) / (sep_len), 2)
        return white_midgame_acc

    @staticmethod
    def end_w_acc(game_move_acc: list) -> float:
        """Calculates the endgame accuracy for white."""
        list_w = game_move_acc[::2]
        end_list_w = np.array_split(list_w, 3)[2]
        sep_len = len(end_list_w)
        if sep_len == 0:
            white_endgame_acc = 0
        else:
            white_endgame_acc = round(sum(end_list_w) / (sep_len), 2)
        return white_endgame_acc

    @staticmethod
    def op_b_acc(game_move_acc: list) -> float:
        """Calculates the opening accuracy for black."""
        list_b = game_move_acc[1::2]
        op_list_b = np.array_split(list_b, 3)[0]
        sep_len = len(op_list_b)
        if sep_len == 0:
            black_opening_acc = 0
        else:
            black_opening_acc = round(sum(op_list_b) / (sep_len), 2)
        return black_opening_acc

    @staticmethod
    def mid_b_acc(game_move_acc: list) -> float:
        """Calculates the opening accuracy for white."""
        list_b = game_move_acc[1::2]
        mid_list_b = np.array_split(list_b, 3)[1]
        sep_len = len(mid_list_b)
        if sep_len == 0:
            black_midgame_acc = 0
        else:
            black_midgame_acc = round(sum(mid_list_b) / (sep_len), 2)
        return black_midgame_acc

    @staticmethod
    def end_b_acc(game_move_acc: list) -> float:
        """Calculates the opening accuracy for white."""
        list_b = game_move_acc[1::2]
        end_list_b = np.array_split(list_b, 3)[2]
        sep_len = len(end_list_b)
        if sep_len == 0:
            black_endgame_acc = 0
        else:
            black_endgame_acc = round(sum(end_list_b) / (sep_len), 2)
        return black_endgame_acc

    @staticmethod
    def w_sec_imp(ow: float, mw: float, ew: float) -> str:
        """Returns the area of improvement for the white player."""
        if mw and ow < ew:
            white_sector_improvement = "Opening"
        elif mw < ow and mw < ew:
            white_sector_improvement = "Midgame"
        else:
            white_sector_improvement = "Endgame"
        return white_sector_improvement

    @staticmethod
    def b_sec_imp(ob: float, mb: float, eb: float) -> str:
        """Returns the area of improvement for the black player."""
        if ob < mb and ob < eb:
            black_sector_improvement = "Opening"
        elif mb < ob and mb < eb:
            black_sector_improvement = "Midgame"
        else:
            black_sector_improvement = "Endgame"
        return black_sector_improvement

    @staticmethod
    def white_castle_move_num(white_castle_num) -> int:
        """
        Returns the move which white castled
        (0 if player didn't castle).
        """
        return sum(white_castle_num)

    @staticmethod
    def black_castle_move_num(black_castle_num) -> int:
        """
        Returns the move which black castled
        (0 if player didn't castle).
        """
        return sum(black_castle_num)

    @staticmethod
    def has_white_castled(white_castle_num) -> int:
        """Checks to see if white castle in the game."""
        if sum(white_castle_num) > 0:
            return 1
        else:
            return 0

    @staticmethod
    def has_black_castled(black_castle_num) -> int:
        """Checks to see if white castle in the game."""
        if sum(black_castle_num) > 0:
            return 1
        else:
            return 0

    @staticmethod
    def white_castle_phase(white_castle_num: list, total_moves: int) -> str:
        """
        Returns the game phase which white castled in -
        returns "None" if player didn't castle.
        """
        if total_moves == 0:
            return "None"
        else:
            if sum(white_castle_num) == 0:
                return "None"
            elif sum(white_castle_num) / (total_moves) < (1 / 3):
                return "Opening"
            elif sum(white_castle_num) / (total_moves) <= (2 / 3):
                return "Midgame"
            elif sum(white_castle_num) / (total_moves) <= 1:
                return "Endgame"

    @staticmethod
    def black_castle_phase(black_castle_num: list, total_moves: int) -> str:
        """
        Returns the game phase which black castled in -
        returns "None" if player didn't castle.
        """
        if total_moves == 0:
            return "None"
        else:
            if sum(black_castle_num) == 0:
                return "None"
            elif sum(black_castle_num) / (total_moves) < (1 / 3):
                return "Opening"
            elif sum(black_castle_num) / (total_moves) <= (2 / 3):
                return "Midgame"
            elif sum(black_castle_num) / (total_moves) <= 1:
                return "Endgame"


class ChessMove(ChessGame):
    """Chess move instance."""

    def __init__(
        self,
        username: str,
        edepth: int,
        start_date: datetime,
        engine: chess.engine.SimpleEngine,
        logger: Logger,
        tot_games: int,
        chess_game: chess.pgn.Game,
        game_num: int,
        board,
        move_num: int,
        game_datetime: datetime,
        gm_mv_num: list,
        gm_mv: list,
        gm_best_mv: list,
        best_move_eval: list,
        mainline_eval: list,
        move_eval_diff: list,
        gm_mv_ac: list,
        move_type_list: list,
        w_castle_num: list,
        b_castle_num: list,
    ):

        ChessGame.__init__(
            self, username, edepth, start_date, engine, game_num, logger, tot_games
        )
        self.chess_game = chess_game
        self.board = board
        self.engine = engine
        self.move_num = move_num
        self.game_datetime = game_datetime
        self.gm_mv_num = gm_mv_num
        self.gm_mv = gm_mv
        self.gm_best_mv = gm_best_mv
        self.best_move_eval = best_move_eval
        self.mainline_eval = mainline_eval
        self.move_eval_diff = move_eval_diff
        self.gm_mv_ac = gm_mv_ac
        self.move_type_list = move_type_list
        self.w_castle_num = w_castle_num
        self.b_castle_num = b_castle_num

    def analyse_move(self, move) -> None:
        """Analyses a users move and exports results to move_data.csv"""
        self.str_bm, self.eval_bm = self.best_move(self.board, self.engine)
        self.str_ml, self.eval_ml = self.mainline_move(move, self.board, self.engine)
        self.evaldiff = self.eval_delta(self.move_num, self.eval_bm, self.eval_ml)
        self.move_acc = self.move_accuracy(self.evaldiff)
        self.move_type = self.assign_move_type(self.move_acc)
        self.square_int = self.get_piece_square_int(move)
        self.curr_board = self.get_curr_board()
        self.piece = self.chess_piece(self.curr_board, self.square_int)
        self.move_col = self.move_colour(self.move_num)
        self.castle_type = self.castling_type(self.piece, self.move_col, self.str_ml)
        self.w_castle_mv_num = self.white_castle_move_num(
            self.castle_type, self.move_num
        )
        self.b_castle_mv_num = self.black_castle_move_num(
            self.castle_type, self.move_num
        )
        self.timers = self.filter_timecont_header(
            self.file_paths.temp,
        )
        self.move_time = self.get_time_spent_on_move(
            self.file_paths.temp, self.move_num, self.timers
        )
        self.move_df = self.create_move_df(
            self.username,
            self.game_datetime,
            self.edepth,
            self.game_num,
            self.move_num,
            self.str_ml,
            self.eval_ml,
            self.str_bm,
            self.eval_bm,
            self.evaldiff,
            self.move_acc,
            self.move_type,
            self.piece,
            self.move_col,
            self.castle_type,
            self.w_castle_mv_num,
            self.b_castle_mv_num,
            self.move_time,
        )
        self.export_move_data(self.move_df, self.username)
        self.append_to_game_lists()

    def mainline_move(
        self, move, board: Board, engine: chess.engine.SimpleEngine
    ) -> tuple:
        """Returns the users move and its evaluation."""
        str_ml = str(move)
        board.push_san(str_ml)
        eval_ml_init = engine.analyse(
            board, chess.engine.Limit(depth=self.edepth), game=object()
        )
        eval_ml = self.move_eval(eval_ml_init)
        return str_ml, eval_ml

    def best_move(self, board: Board, engine: chess.engine.SimpleEngine) -> tuple:
        """Returns the best move from the engine and its evaluation."""
        best_move = engine.play(
            board, chess.engine.Limit(depth=self.edepth), game=object()
        )
        str_bm = str(best_move.move)
        board.push_san(str_bm)
        eval_bm_init = engine.analyse(
            board, chess.engine.Limit(depth=self.edepth), game=object()
        )
        eval_bm = self.move_eval(eval_bm_init)
        board.pop()
        return str_bm, eval_bm

    @staticmethod
    def move_eval(move) -> None:
        """Returns the evalaution of the move played."""
        get_eval = str(move["score"].white())
        if "#" in get_eval:
            get_eval = get_eval[1:]
        else:
            get_eval = get_eval
        get_eval = int(get_eval)
        return get_eval

    @staticmethod
    def eval_delta(move_num, eval_bm, eval_ml) -> float:
        """Returns the eval difference between the best and mainline move."""
        if move_num % 2 == 0:
            eval_diff = round(abs(eval_bm - eval_ml), 3)
            return eval_diff
        else:
            eval_diff = round(abs(eval_ml - eval_bm), 3)
            return eval_diff

    @staticmethod
    def move_accuracy(eval_diff) -> float:
        """Returns the move accuracy for a given move."""
        m, v = 0, 1.5
        move_acc = round(math.exp(-0.00003 * ((eval_diff - m) / v) ** 2) * 100, 1)
        return move_acc

    @staticmethod
    def assign_move_type(move_acc) -> int:
        """Returns the move type for a given move."""
        # best = 2, excellent = 1, good = 0,
        # inacc = -1, mistake = -2, blunder = -3, missed win = -4
        if move_acc == 100:
            move_type = 2
        elif 99.5 <= move_acc < 100:
            move_type = 1
        elif 87.5 <= move_acc < 99.5:
            move_type = 0
        elif 58.6 <= move_acc < 87.5:
            move_type = -1
        elif 30 <= move_acc < 58.6:
            move_type = -2
        elif 2 <= move_acc < 30:
            move_type = -3
        else:
            move_type = -4
        return move_type

    @staticmethod
    def chess_piece(curr_board, square_int) -> str:
        """Returns the piece type for the move played."""
        piece_type_num = chess.BaseBoard.piece_type_at(curr_board, square_int)
        if piece_type_num == 1:
            piece_type = "pawn"
        elif piece_type_num == 2:
            piece_type = "knight"
        elif piece_type_num == 3:
            piece_type = "bishop"
        elif piece_type_num == 4:
            piece_type = "rook"
        elif piece_type_num == 5:
            piece_type = "queen"
        elif piece_type_num == 6:
            piece_type = "king"
        else:
            piece_type = " "
        return piece_type

    def get_curr_board(self) -> chess.BaseBoard:
        """Returns the current board."""
        curr_fen = self.board.board_fen()
        curr_board = chess.BaseBoard(board_fen=curr_fen)
        return curr_board

    @staticmethod
    def get_piece_square_int(move) -> int:
        """
        Returns an integer between 0-63 which represents
        the pieces position on the board.
        """
        piece_col = str(move)[2:3]
        piece_row = str(move)[3:4]
        piece_square = str(piece_col + piece_row)
        square_int = chess.parse_square(piece_square)
        return square_int

    @staticmethod
    def move_colour(move_num) -> str:
        """Returns the current moves colour."""
        if move_num % 2 == 0:
            mv_colour = "white"
        else:
            mv_colour = "black"
        return mv_colour

    @staticmethod
    def castling_type(piece, move_col, str_ml) -> str:
        """Returns the type of castling - None if current move isnt castle."""
        if piece == "king" and move_col == "white" and str_ml == "e1g1":
            cas_type = "white_short"
        elif piece == "king" and move_col == "white" and str_ml == "e1c1":
            cas_type = "white_long"
        elif piece == "king" and move_col == "black" and str_ml == "e8g8":
            cas_type = "black_short"
        elif piece == "king" and move_col == "black" and str_ml == "e8c8":
            cas_type = "black_long"
        else:
            cas_type = None
        return cas_type

    @staticmethod
    def white_castle_move_num(castle_type, move_num) -> int:
        """Move which white castled in the game."""
        if castle_type == "white_short" or castle_type == "white_long":
            white_castle_move = move_num
        else:
            white_castle_move = 0
        return white_castle_move

    @staticmethod
    def black_castle_move_num(castle_type, move_num) -> int:
        """Move which black castled in the game."""
        if castle_type == "black_short" or castle_type == "black_long":
            black_castle_move = move_num
        else:
            black_castle_move = 0
        return black_castle_move

    @staticmethod
    def get_time_spent_on_move(
        tempfilepath: str, move_num: int, timers: tuple
    ) -> float:
        """Calculated the time the player spent on the current move."""
        chess_game_pgn = open(tempfilepath)
        game = chess.pgn.read_game(chess_game_pgn)
        timerem_w, timerem_b, time_int = timers[0], timers[1], timers[2]
        time_list = []
        for num, move in enumerate(game.mainline()):
            if num % 2 == 0:
                move_time_w = move.clock()
                time_spent = round(timerem_w - move_time_w + time_int, 3)
                time_list.append(time_spent)
                timerem_w = move_time_w
            else:
                move_time_b = move.clock()
                time_spent = round(timerem_b - move_time_b + time_int, 3)
                time_list.append(time_spent)
                timerem_b = move_time_b
        return time_list[int(move_num)]

    @staticmethod
    def filter_timecont_header(tempfilepath: str) -> tuple[float, float, int]:
        """
        Filters time control headers if time control contains move interval.
        """
        chess_game_pgn = open(tempfilepath)
        game = chess.pgn.read_game(chess_game_pgn)
        tc_white = game.headers["TimeControl"]
        tc_black = game.headers["TimeControl"]
        if ("+" in tc_white) or ("+" in tc_black):
            time_interval = int(tc_white.split("+")[1])
            tc_white = float(tc_white.split("+")[0])
            tc_black = float(tc_black.split("+")[0])
            return (tc_white, tc_black, time_interval)
        else:
            try:
                tc_white = float(tc_white)
                tc_black = float(tc_black)
                time_interval = 0
                return (tc_white, tc_black, time_interval)
            except ValueError:
                tc_white = 180.0
                tc_black = 180.0
                time_interval = 0
                return (tc_white, tc_black, time_interval)

    def create_move_df(
        self,
        username: str,
        game_datetime: datetime,
        edepth: int,
        game_num: int,
        move_num: int,
        str_ml: str,
        eval_ml: int,
        str_bm: str,
        eval_bm: int,
        evaldiff: int,
        move_acc: float,
        move_type: int,
        piece: str,
        move_col: str,
        castle_type: str,
        w_castle_mv_num: int,
        b_castle_mv_num: int,
        move_time: float,
    ) -> pd.DataFrame:
        self.move_df = pd.DataFrame(
            {
                "Username": username,
                "Game_date": game_datetime,
                "Engine_depth": edepth,
                "Game_number": game_num,
                "Move_number": move_num,
                "Move": str_ml,
                "Move_eval": eval_ml,
                "Best_move": str_bm,
                "Best_move_eval": eval_bm,
                "Move_eval_diff": evaldiff,
                "Move_accuracy": move_acc,
                "Move_type": move_type,
                "Piece": piece,
                "Move_colour": move_col,
                "Castling_type": castle_type,
                "White_castle_num": w_castle_mv_num,
                "Black_castle_num": b_castle_mv_num,
                "Move_time": move_time,
            },
            index=[0],
        )
        return self.move_df

    def export_move_data(self, move_df: pd.DataFrame, username: str) -> None:
        "Exports the move date to a sqlite3 server."
        conn = sqlite3.connect(FileHandler(username=self.username).db_location)
        move_df.to_sql("move_data", conn, if_exists="append", index=False)
        conn.commit
        conn.close

    def append_to_game_lists(self) -> None:
        self.gm_mv_num.append(self.move_num)
        self.gm_mv.append(self.str_ml)
        self.gm_best_mv.append(self.str_bm)
        self.best_move_eval.append(self.eval_bm)
        self.mainline_eval.append(self.eval_ml)
        self.move_eval_diff.append(self.evaldiff)
        self.gm_mv_ac.append(self.move_acc)
        self.move_type_list.append(self.move_type)
        self.w_castle_num.append(self.w_castle_mv_num)
        self.b_castle_num.append(self.b_castle_mv_num)


class ChessGameHeaders(ChessGame):
    def __init__(
        self,
        username,
        edepth,
        start_date,
        engine,
        game_num,
        logger,
        tot_games,
        chess_game,
    ):
        ChessGame.__init__(
            self, username, edepth, start_date, engine, game_num, logger, tot_games
        )
        self.chess_game = chess_game
        self.engine = engine
        self.game_date = self.game_dt(self.chess_game)
        self.game_time = self.game_t(self.chess_game)
        self.game_datetime = self.game_dt_time(self.game_date, self.game_time)
        self.time_cont = self.time_control(self.chess_game)
        self.white = self.player_white(self.chess_game)
        self.black = self.player_black(self.chess_game)
        self.player = self.user_colour(self.white, self.username)
        self.ratingwhite = self.rating_white(self.chess_game)
        self.ratingblack = self.rating_black(self.chess_game)
        self.opening_class = self.opening_cls(self.chess_game)
        self.opening_name = self.opening_nm(self.chess_game)
        self.termination = self.game_termination(self.chess_game, self.username)
        self.end_type = self.win_draw_loss(self.chess_game)
        self.user_rating = self.rating_user(
            self.player, self.ratingwhite, self.ratingblack
        )
        self.opp_rating = self.rating_opponent(
            self.player, self.ratingwhite, self.ratingblack
        )
        self.user_winner = self.user_winr(self.player, self.end_type)

    def collect_headers(self) -> dict:
        """Dictionary of all the headers required for analysis."""
        header_dict = {
            "Game_date": self.game_date,
            "Game_time": self.game_time,
            "Game_datetime": self.game_datetime,
            "Time_control": self.time_cont,
            "Username": self.username,
            "User_Colour": self.player,
            "User_rating": self.user_rating,
            "Opponent_rating": self.opp_rating,
            "User_winner": self.user_winner,
            "White_player": self.white,
            "Black_player": self.black,
            "White_rating": self.ratingwhite,
            "Black_rating": self.ratingblack,
            "Opening_class": self.opening_class,
            "Opening_name": self.opening_name,
            "Termination": self.termination,
            "Win_draw_loss": self.end_type,
        }
        return header_dict

    def time_control(self, chess_game) -> str:
        """Returns the time control header."""
        time_cont = chess_game.headers["TimeControl"]
        return time_cont

    def player_white(self, chess_game) -> str:
        """Returns the white player header."""
        white = chess_game.headers["White"]
        return white

    def player_black(self, chess_game) -> str:
        """Returns the black player header."""
        black = chess_game.headers["Black"]
        return black

    def user_colour(self, white, username) -> str:
        """Returns the user colour."""
        player = "White" if white == username else "Black"
        return player

    def rating_white(self, chess_game) -> int:
        "Returns the white rating header."
        ratingwhite = int(chess_game.headers["WhiteElo"])
        return ratingwhite

    def rating_black(self, chess_game) -> int:
        "Returns the black rating header."
        ratingblack = int(chess_game.headers["BlackElo"])
        return ratingblack

    def opening_cls(self, chess_game) -> str:
        """Returns the opening class of the current game."""
        try:
            opening_class = chess_game.headers["ECO"]
        except KeyError:
            opening_class = "000"
        return opening_class

    def opening_nm(self, chess_game) -> str:
        """Returns the opening name of the current game."""
        try:
            opening_name_raw = chess_game.headers["ECOUrl"]
        except KeyError:
            opening_name_raw = "/NA"
        opening_string = opening_name_raw.split("/")[-1]
        opening_name = str(opening_string.replace("-", " ").strip())
        return opening_name

    def game_termination(self, chess_game, username) -> str:
        """Returns the termination (way the game ended) header."""
        termination_raw = chess_game.headers["Termination"]
        winner_check = termination_raw.split(" ")
        draw_check = " ".join(winner_check[0:2])
        if winner_check[0] == username:
            termination = "Win " + " ".join(winner_check[2:])
        elif draw_check == "Game drawn":
            termination = "Draw " + " ".join(winner_check[2:])
        else:
            termination = "Loss " + " ".join(winner_check[2:])
        return termination

    def rating_user(self, player, rating_w, rating_b) -> int:
        """Returns the users rating."""
        user_rating = rating_w if player == "White" else rating_b
        return user_rating

    def rating_opponent(self, player, rating_w, rating_b) -> int:
        """Returns the oppenents rating."""
        opp_rating = rating_b if player == "White" else rating_w
        return opp_rating

    def win_draw_loss(self, chess_game) -> str:
        """Returns whether the user won, drew or lost the current game."""
        if chess_game.headers["Result"] == "1-0":
            end_type = "White"
        elif chess_game.headers["Result"] == "0-1":
            end_type = "Black"
        else:
            end_type = "Draw"
        return end_type

    def user_winr(self, winner, player) -> str:
        """Returns whether the user won, drew or lost the current game."""

        pww = winner == "White" and player == "White"
        pbw = winner == "Black" and player == "Black"
        pwl = winner == "Black" and player == "White"
        pbl = winner == "White" and player == "Black"
        if pww or pbw:
            user_winner = "Win"
        elif pwl or pbl:
            user_winner = "Loss"
        else:
            user_winner = "Draw"
        return user_winner

    def game_dt(self, chess_game) -> str:
        """Returns the current game date."""
        game_date = chess_game.headers["UTCDate"]
        return game_date

    def game_t(self, chess_game) -> str:
        """Returns the current game time."""
        game_time = chess_game.headers["UTCTime"]
        return game_time

    def game_dt_time(self, game_date, game_time) -> datetime:
        """returns the datetime of the current game."""
        game_date_time = f"{game_date} {game_time}"
        game_datetime = datetime.strptime(game_date_time, "%Y.%m.%d %H:%M:%S")
        return game_datetime


class FileHandler:
    """Storage location for the data/lib/log filepaths."""

    def __init__(self, username: str):
        self.username = username
        self.dir = os.path.dirname(__file__)
        stockfish_path = r"../lib/stkfsh_14.1/stk_14.1.exe"
        self.stockfish = os.path.join(self.dir, stockfish_path)
        self.userlogfile = os.path.join(self.dir, rf"../logs/{self.username}.log")
        self.temp = os.path.join(self.dir, r"../data/temp.pgn")
        self.move_data = os.path.join(self.dir, r"../data/move_data.csv")
        self.game_data = os.path.join(self.dir, r"../data/game_data.csv")
        self.pgn_data = os.path.join(
            self.dir, rf"../data/pgn_data/{self.username}_pgn_data.csv"
        )
        self.db_location = "./data/betterchess.db"


class InputHandler:
    """Class for determining input arguments for the user class."""

    @staticmethod
    def get_inputs() -> dict:
        print("==============================================================")
        username = InputHandler.user_input()
        edepth = InputHandler.depth_input()
        start_year = InputHandler.year_input()
        start_month = InputHandler.month_input()
        start_date = InputHandler.start_datetime(start_year, start_month)
        print("==============================================================")
        return {"username": username, "edepth": edepth, "start_date": start_date}

    # chessdotcom.types.ChessDotComError:

    @staticmethod
    def user_input() -> str:
        username = input("Enter your username: ")

        return username

    @staticmethod
    def depth_input() -> str:
        edepth = input("Enter the engine depth (1-20): ")

        return edepth

    @staticmethod
    def year_input() -> str:
        start_year = input("Enter the start year for analysis (e.g. 2020): ")

        return start_year

    @staticmethod
    def month_input() -> str:
        start_month = input("Enter the start month for analysis (e.g. 01): ")
        return start_month

    @staticmethod
    def start_datetime(start_year: str, start_month: str) -> datetime:
        start_datetime = start_year + "-" + start_month + "-01" + " 00:00:00"
        start_date = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")
        return start_date

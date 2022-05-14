import chess
import chess.engine
import chess.pgn
import math
import os
import logging
import analysis_filter
import numpy as np
import pandas as pd
import time
import progress
import extract
import regex as re
from datetime import datetime
from logging import Logger

class ChessUser:
    def __init__(self, username: str, edepth: int, start_date: datetime):
        self.username = username
        self.edepth = edepth
        self.start_date = start_date
        self.file_paths = FileHandler(username=self.username)

    def create_logger(self) -> Logger:
        logging.basicConfig(
            filename=self.file_paths.userlogfile,
            format='[%(levelname)s %(module)s] %(message)s',
            level=logging.INFO, datefmt='%Y/%m/%d %I:%M:%S')
        self.logger = logging.getLogger(__name__)
        return self.logger

    def create_engine(self) -> chess.engine.SimpleEngine:
        self.engine = chess.engine.SimpleEngine.popen_uci(
            self.file_paths.stockfish)
        return self.engine

    def run_analysis(self) -> None:
        extract.data_extract(
            self.username,
            self.file_paths.pgn_data,
            self.file_paths.userlogfile,
            self.logger)
        self.analyse_user()

    def analyse_user(self) -> None:
        all_games_data = pd.read_csv(
            self.file_paths.pgn_data, delimiter="|",
            names=["url_date", "game_data"])
        self.tot_games = len(all_games_data["game_data"])
        print("Analysing users data: ")
        analysis_filter.clean_movecsv(self.file_paths.move_data,
                                      self.file_paths.userlogfile)
        for game_num, chess_game in enumerate(all_games_data["game_data"]):
            with open(self.file_paths.temp, "w") as temp_pgn:
                temp_pgn.write(str(chess_game.replace(" ; ", "\n")))
            game = ChessGame(self.username, self.edepth,
                             self.start_date, self.engine,
                             game_num, self.logger, self.tot_games)
            game.run_game_analysis()


class ChessGame(ChessUser):
    def __init__(
            self, username: str, edepth: int,
            start_date: datetime, engine: chess.engine.SimpleEngine,
            game_num: int, logger: Logger,
            tot_games: int):
        super().__init__(username, edepth, start_date)
        self.engine = engine
        self.game_num = game_num
        self.logger = logger
        self.tot_games = tot_games

    def init_game_analysis(self) -> None:
        self.init_game()
        self.init_board()
        self.init_game_lists()
        game_headers = ChessGameHeaders(
            self.username, self.edepth,
            self.start_date, self.engine,
            self.game_num, self.logger,
            self.tot_games, self.chess_game)
        self.headers = game_headers.collect_headers()
        self.game_dt = game_headers.collect_headers()["Game_datetime"]
        self.game_analysis_filter()

    def run_game_analysis(self) -> None:
        self.init_game_analysis()
        if self.game_dt >= self.log_dt:
            start = time.perf_counter()
            self.logger.info(f"| {self.game_dt} |{self.game_num}")
            for move_num, move in enumerate(self.chess_game.mainline_moves()):
                chess_move = ChessMove(
                    self.username, self.edepth, self.start_date,
                    self.engine, self.logger, self.tot_games, self.game_num,
                    self.board, move_num, self.game_dt, self.gm_mv_num,
                    self.gm_mv, self.gm_best_mv, self.best_move_eval,
                    self.mainline_eval, self.move_eval_diff,
                    self.gm_mv_ac, self.move_type_list)
                chess_move.analyse_move(move)
            try:
                self.total_moves = math.ceil(move_num/2)
            except UnboundLocalError:
                self.total_moves = 0
            self.analyse_game()
            end = time.perf_counter()
            progress.progress_bar(self.game_num, self.tot_games,
                                  start, end)

    def analyse_game(self) -> None:
        self.sum_type_dict = self.sum_move_types()
        self.user_game_data()
        self.export_game_data()

    def game_analysis_filter(self) -> None:
        analysis_filter.init_game_logs(
            self.file_paths.userlogfile,
            self.logger)
        self.log_dt = analysis_filter.llog_game(self.file_paths.userlogfile)

    def init_game(self):
        self.chess_game_pgn = open(self.file_paths.temp)
        self.chess_game = chess.pgn.read_game(self.chess_game_pgn)
        return self.chess_game

    def init_board(self):
        self.board = self.chess_game.board()
        return self.board

    def init_game_lists(self) -> None:
        self.gm_mv_num = []
        self.gm_mv = []
        self.gm_best_mv = []
        self.best_move_eval = []
        self.mainline_eval = []
        self.move_eval_diff = []
        self.gm_mv_ac = []
        self.move_type_list = []

    def export_game_data(self) -> None:
        "Exports the move date to a csv."
        game_df = pd.DataFrame({
            "Username": self.username,
            "Date": self.game_dt,
            "Engine_depth": self.edepth,
            "Game_number": self.game_num,
            "Game_type": self.headers["Time_control"],
            "White_player": self.headers["White_player"],
            "Black_player": self.headers["Black_player"],
            "White_rating": self.headers["White_rating"],
            "Black_rating": self.headers["Black_rating"],
            "User_colour": self.headers["User_Colour"],
            "User_rating": self.headers["User_rating"],
            "opponent_rating": self.headers["Opponent_rating"],
            "User_winner": self.headers["User_winner"],
            "Opening_name": self.headers["Opening_name"],
            "Opening_class": self.headers["Opening_class"],
            "Termination": self.headers["Termination"],
            "End_type": self.headers["Win_draw_loss"],
            "Number_of_moves": self.total_moves,
            "Accuracy": self.gm_acc,
            "Opening_accuracy": self.o_acc,
            "Mid_accuracy": self.m_acc,
            "End_accuracy": self.e_acc,
            "No_best": self.no_best,
            "No_great": self.no_excl,
            "No_good": self.no_good,
            "No_inaccuracy": self.no_inac,
            "No_mistake": self.no_mist,
            "No_blunder": self.no_blun,
            "No_missed_win": self.no_misw,
            "Improvement": self.improve},
            index=[0])
        game_df.to_csv(
            self.file_paths.game_data, mode='a',
            header=False, index=False)

    def user_game_data(self) -> None:
        if self.username == self.headers["White_player"]:
            self.gm_acc = self.game_w_acc()
            self.o_acc = self.op_w_acc()
            self.m_acc = self.mid_w_acc()
            self.e_acc = self.end_w_acc()
            self.no_best = self.move_dict["No_w_best"]
            self.no_excl = self.move_dict["No_w_excl"]
            self.no_good = self.move_dict["No_w_good"]
            self.no_inac = self.move_dict["No_w_inac"]
            self.no_mist = self.move_dict["No_w_mist"]
            self.no_blun = self.move_dict["No_w_blun"]
            self.no_misw = self.move_dict["No_w_misw"]
            self.improve = self.w_sec_imp()
        else:
            self.gm_acc = self.game_b_acc()
            self.o_acc = self.op_b_acc()
            self.m_acc = self.mid_b_acc()
            self.e_acc = self.end_b_acc()
            self.no_best = self.move_dict["No_b_best"]
            self.no_excl = self.move_dict["No_b_excl"]
            self.no_good = self.move_dict["No_b_good"]
            self.no_inac = self.move_dict["No_b_inac"]
            self.no_mist = self.move_dict["No_b_mist"]
            self.no_blun = self.move_dict["No_b_blun"]
            self.no_misw = self.move_dict["No_b_misw"]
            self.improve = self.b_sec_imp()

    def sum_move_types(self) -> dict:
        '''Returns the number of best moves for black and white.'''
        self.w_best = self.move_type_list[::2].count(2)
        self.b_best = self.move_type_list[1::2].count(2)
        self.w_excl = self.move_type_list[::2].count(1)
        self.w_excl = self.move_type_list[1::2].count(1)
        self.w_good = self.move_type_list[::2].count(0)
        self.b_good = self.move_type_list[1::2].count(0)
        self.w_inac = self.move_type_list[::2].count(-1)
        self.b_inac = self.move_type_list[1::2].count(-1)
        self.w_mist = self.move_type_list[::2].count(-2)
        self.b_mist = self.move_type_list[1::2].count(-2)
        self.w_blun = self.move_type_list[::2].count(-3)
        self.b_blun = self.move_type_list[1::2].count(-3)
        self.w_misw = self.move_type_list[::2].count(-4)
        self.b_misw = self.move_type_list[1::2].count(-4)
        self.move_dict = {
            "No_w_best": self.w_best, "No_b_best": self.b_best,
            "No_w_excl": self.w_excl, "No_b_excl": self.w_excl,
            "No_w_good": self.w_good, "No_b_good": self.b_good,
            "No_w_inac": self.w_inac, "No_b_inac": self.b_inac,
            "No_w_mist": self.w_mist, "No_b_mist": self.b_mist,
            "No_w_blun": self.w_blun, "No_b_blun": self.b_blun,
            "No_w_misw": self.w_misw, "No_b_misw": self.b_misw}
        return self.move_dict

    def game_w_acc(self) -> float:
        '''returns white players game accuracy.'''
        w_list = self.gm_mv_ac[::2]
        list_len = len(self.gm_mv_ac[::2])
        if list_len == 0:
            self.wg_acc = 0
        else:
            self.wg_acc = round(sum(w_list) / list_len, 2)
        return self.wg_acc

    def game_b_acc(self) -> float:
        '''returns black players game accuracy.'''
        b__list = self.gm_mv_ac[1::2]
        list_len = len(self.gm_mv_ac[1::2])
        if list_len == 0:
            self.bg_acc = 0
        else:
            self.bg_acc = round(sum(b__list) / list_len, 2)
        return self.bg_acc

    def op_w_acc(self) -> float:
        '''Calculates the opening accuracy white.'''
        list_w = self.gm_mv_ac[::2]
        sep_len = len(np.array_split(list_w, 3)[0])
        if sep_len == 0:
            self.ow = 0
        else:
            self.ow = round(sum(list_w) / (sep_len*3), 2)
        return self.ow

    def mid_w_acc(self) -> float:
        '''Calculates the midgame accuracy white.'''
        list_w = self.gm_mv_ac[::2]
        sep_len = len(np.array_split(list_w, 3)[1])
        if sep_len == 0:
            self.mw = 0
        else:
            self.mw = round(sum(list_w) / (sep_len*3), 2)
        return self.mw

    def end_w_acc(self) -> float:
        '''Calculates the endgame accuracy white.'''
        list_w = self.gm_mv_ac[::2]
        sep_len = len(np.array_split(list_w, 3)[2])
        if sep_len == 0:
            self.ew = 0
        else:
            self.ew = round(sum(list_w) / (sep_len*3), 2)
        return self.ew

    def op_b_acc(self) -> float:
        '''Calculates the opening accuracy black.'''
        list_b = self.gm_mv_ac[1::2]
        sep_len = len(np.array_split(list_b, 3)[0])
        if sep_len == 0:
            self.ob = 0
        else:
            self.ob = round(sum(list_b) / (sep_len*3), 2)
        return self.ob

    def mid_b_acc(self) -> float:
        '''Calculates the opening accuracy white.'''
        list_b = self.gm_mv_ac[1::2]
        sep_len = len(np.array_split(list_b, 3)[1])
        if sep_len == 0:
            self.mb = 0
        else:
            self.mb = round(sum(list_b) / (sep_len*3), 2)
        return self.mb

    def end_b_acc(self) -> float:
        '''Calculates the opening accuracy white.'''
        list_b = self.gm_mv_ac[1::2]
        sep_len = len(np.array_split(list_b, 3)[2])
        if sep_len == 0:
            self.eb = 0
        else:
            self.eb = round(sum(list_b) / (sep_len*3), 2)
        return self.eb

    def w_sec_imp(self) -> str:
        '''Returns the area of improvement for the white player'''
        # White
        if self.ow < self.mw and self.ow < self.ew:
            self.imp_w = "Opening"
        elif self.mw < self.ow and self.mw < self.ew:
            self.imp_w = "Midgame"
        else:
            self.imp_w = "Endgame"
        return self.imp_w

    def b_sec_imp(self) -> str:
        '''Returns the area of improvement for the black player'''
        if self.ob < self.mb and self.ob < self.eb:
            self.imp_b = "Opening"
        elif self.mb < self.ob and self.mb < self.eb:
            self.imp_b = "Midgame"
        else:
            self.imp_b = "Endgame"
        return self.imp_b


class ChessMove(ChessGame):
    """Chess move instance."""
    def __init__(
        self, username: str, edepth: int, start_date: datetime,
        engine: chess.engine.SimpleEngine, logger: Logger, tot_games: int,
        game_num: int, board, move_num: int,
        game_datetime: datetime, gm_mv_num: list, gm_mv: list,
        gm_best_mv: list, best_move_eval: list, mainline_eval: list,
        move_eval_diff: list, gm_mv_ac: list, move_type_list: list):
        ChessGame.__init__(self, username, edepth,
                           start_date, engine, game_num, logger, tot_games)
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

    def analyse_move(self, move) -> None:
        """Analyses a users move and exports results to move_data.csv"""
        self.str_bm, self.eval_bm = self.best_move()
        self.str_ml, self.eval_ml = self.mainline_move(move)
        self.evaldiff = self.eval_delta(
            self.move_num, self.eval_bm, self.eval_ml)
        self.move_acc = self.move_accuracy(self.evaldiff)
        self.move_type = self.assign_move_type(self.move_acc)
        self.export_move_data()
        self.append_to_game_lists()

    def mainline_move(self, move) -> tuple:
        """Returns the users move and its evaluation."""
        self.str_ml = str(move)
        self.board.push_san(self.str_ml)
        eval_ml_init = self.engine.analyse(
            self.board,
            chess.engine.Limit(depth=self.edepth),
            game=object())
        self.eval_ml = self.move_eval(eval_ml_init)
        return self.str_ml, self.eval_ml

    def best_move(self) -> tuple:
        """Returns the best move from the engine and its evaluation."""
        best_move = self.engine.play(
            self.board,
            chess.engine.Limit(depth=self.edepth),
            game=object())
        self.str_bm = str(best_move.move)
        self.board.push_san(self.str_bm)
        eval_bm_init = self.engine.analyse(
            self.board,
            chess.engine.Limit(depth=self.edepth),
            game=object())
        self.eval_bm = self.move_eval(eval_bm_init)
        self.board.pop()
        return self.str_bm, self.eval_bm

    def move_eval(self, move) -> None:
        '''Returns the evalaution of the move played.'''
        get_eval = str(move['score'].white())
        if "#" in get_eval:
            get_eval = get_eval[1:]
        else:
            get_eval = get_eval
        get_eval = int(get_eval)
        return get_eval

    def eval_delta(self, move_num, eval_bm, eval_ml) -> float:
        '''Returns the eval difference between the best and mainline move.'''
        if move_num % 2 == 0:
            eval_diff = round(abs(eval_bm - eval_ml), 3)
            return eval_diff
        else:
            eval_diff = round(abs(eval_ml - eval_bm), 3)
            return eval_diff

    def move_accuracy(self, eval_diff) -> float:
        '''Returns the move accuracy for a given move.'''
        m, v = 0, 1.5
        move_acc = round(math.exp(-0.00003*((eval_diff-m)/v)**2)*100, 1)
        return move_acc

    def assign_move_type(self, move_acc) -> int:
        '''Returns the move type for a given move.'''
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

    def export_move_data(self) -> None:
        "Exports the move date to a csv."
        move_df = pd.DataFrame({
            "Username": self.username,
            "Game_date": self.game_datetime,
            "edepth": self.edepth,
            "Game_number": self.game_num,
            "Move_number": self.move_num,
            "Move": self.str_ml,
            "Move_eval": self.eval_ml,
            "Best_move": self.str_bm,
            "Best_move_eval": self.eval_bm,
            "Move_eval_diff": self.evaldiff,
            "Move accuracy": self.move_acc,
            "Move_type": self.move_type,
            }, index=[0])
        move_df.to_csv(
            self.file_paths.move_data, mode='a',
            header=False, index=False)

    def append_to_game_lists(self) -> None:
        self.gm_mv_num.append(self.move_num)
        self.gm_mv.append(self.str_ml)
        self.gm_best_mv.append(self.str_bm)
        self.best_move_eval.append(self.eval_bm)
        self.mainline_eval.append(self.eval_ml)
        self.move_eval_diff.append(self.evaldiff)
        self.gm_mv_ac.append(self.move_acc)
        self.move_type_list.append(self.move_type)


class ChessGameHeaders(ChessGame):
    def __init__(self, username, edepth, start_date,
                 engine, game_num, logger, tot_games, chess_game):
        ChessGame.__init__(self, username, edepth,
                           start_date, engine, game_num, logger, tot_games)
        self.chess_game = chess_game
        self.engine = engine

    def collect_headers(self) -> dict:
        header_dict = {
            "Game_date": self.game_dt(self.chess_game),
            "Game_time": self.game_t(self.chess_game),
            "Game_datetime": self.game_dt_time(),
            "Time_control": self.time_control(self.chess_game),
            "Username": self.username,
            "User_Colour": self.user_colour(),
            "User_rating": self.rating_user(),
            "Opponent_rating": self.rating_opponent(),
            "User_winner": self.user_winr(),
            "White_player": self.player_white(self.chess_game),
            "Black_player": self.player_black(self.chess_game),
            "White_rating": self.rating_white(self.chess_game),
            "Black_rating": self.rating_black(self.chess_game),
            "Opening_class": self.opening_cls(self.chess_game),
            "Opening_name": self.opening_nm(self.chess_game),
            "Termination": self.game_termination(self.chess_game),
            "Win_draw_loss": self.win_draw_loss(self.chess_game)}
        return header_dict

    def time_control(self, chess_game) -> str:
        self.game_time_cont = chess_game.headers["TimeControl"]
        return self.game_time_cont

    def player_white(self, chess_game) -> str:
        self.white = chess_game.headers["White"]
        return self.white

    def player_black(self, chess_game) -> str:
        self.black = chess_game.headers["Black"]
        return self.black

    def user_colour(self) -> str:
        white = self.player_white(self.chess_game)
        self.player = "White" if white == self.username else "Black"
        return self.player

    def rating_white(self, chess_game) -> int:
        self.ratingwhite = int(chess_game.headers["WhiteElo"])
        return self.ratingwhite

    def rating_black(self, chess_game) -> int:
        self.ratingblack = int(chess_game.headers["BlackElo"])
        return self.ratingblack

    def opening_cls(self, chess_game) -> str:
        try:
            self.opening_class = chess_game.headers["ECO"]
        except KeyError:
            self.opening_class = "000"
        return self.opening_class

    def opening_nm(self, chess_game) -> str:
        try:
            opening_name_raw = chess_game.headers["ECOUrl"]
        except KeyError:
            opening_name_raw = "/NA"
        opening_string = opening_name_raw.split("/")[-1]
        self.opening_name = str(opening_string.replace("-", " ").strip())
        return self.opening_name

    def game_termination(self, chess_game) -> str:
        termination_raw = chess_game.headers["Termination"]
        winner_check = termination_raw.split(" ")
        draw_check = " ".join(winner_check[0:2])
        if winner_check[0] == self.username:
            self.termination = "Win " + " ".join(winner_check[2:])
        elif draw_check == "Game drawn":
            self.termination = "Draw " + " ".join(winner_check[2:])
        else:
            self.termination = "Loss " + " ".join(winner_check[2:])
        return self.termination

    def rating_user(self) -> int:
        player = self.user_colour()
        rating_w = self.rating_white(self.chess_game)
        rating_b = self.rating_black(self.chess_game)
        self.user_rating = rating_w if player == "White" else rating_b
        return self.user_rating

    def rating_opponent(self) -> int:
        player = self.user_colour()
        rating_w = self.rating_white(self.chess_game)
        rating_b = self.rating_black(self.chess_game)
        self.opp_rating = rating_b if player == "White" else rating_w
        return self.opp_rating

    def win_draw_loss(self, chess_game) -> str:
        if chess_game.headers["Result"] == "1-0":
            self.end_type = "White"
        elif chess_game.headers["Result"] == "0-1":
            self.end_type = "Black"
        else:
            self.end_type = "Draw"
        return self.end_type

    def user_winr(self) -> str:
        winner = self.win_draw_loss(self.chess_game)
        player = self.user_colour()
        pww = (winner == "White" and player == "White")
        pbw = (winner == "Black" and player == "Black")
        pwl = (winner == "Black" and player == "White")
        pbl = (winner == "White" and player == "Black")
        if pww or pbw:
            self.user_winner = "Win"
        elif pwl or pbl:
            self.user_winner = "Loss"
        else:
            self.user_winner = "Draw"
        return self.user_winner

    def game_dt(self, chess_game) -> str:
        self.game_date = chess_game.headers["UTCDate"]
        return self.game_date

    def game_t(self, chess_game) -> str:
        self.game_time = chess_game.headers["UTCTime"]
        return self.game_time

    def game_dt_time(self) -> datetime:
        game_date = self.game_dt(self.chess_game)
        game_time = self.game_t(self.chess_game)
        game_date_time = f"{game_date} {game_time}"
        self.game_datetime = datetime.strptime(
            game_date_time,
            '%Y.%m.%d %H:%M:%S')
        return self.game_datetime


class FileHandler:
    """Storage location for the data/lib/log filepaths."""
    def __init__(self, username: str):
        self.username = username
        self.dir = os.path.dirname(__file__)
        stockfish_path = r"../lib/stkfsh_14.1/stockfish_14.1_win_x64_avx2.exe"
        self.stockfish = os.path.join(self.dir, stockfish_path)
        self.userlogfile = os.path.join(
            self.dir,
            rf"../logs/{self.username}.log")
        self.temp = os.path.join(self.dir, r"../data/temp.pgn")
        self.move_data = os.path.join(self.dir, r"../data/move_data.csv")
        self.game_data = os.path.join(self.dir, r"../data/game_data.csv")
        self.pgn_data = os.path.join(
            self.dir,
            rf"../data/pgn_data/{self.username}_pgn_data.csv")


class InputHandler:
    """Class for determining input arguments for the user class."""
    @staticmethod
    def get_inputs() -> dict:
        print("============================================================================")
        username = InputHandler.user_input()
        edepth = InputHandler.depth_input()
        start_year = InputHandler.year_input()
        start_month = InputHandler.month_input()
        start_date = InputHandler.start_datetime(start_year, start_month)
        print("============================================================================")
        return {"username": username,
                "edepth": edepth,
                "start_date": start_date}

    @staticmethod
    def user_input():
        username = input("Enter your username: ")
        if len(username) == 0:
            print("Please enter a valid username")
            InputHandler.user_input()
        if not isinstance(username, str):
            print("Please enter a valid username")
            InputHandler.user_input()
        return username

    @staticmethod
    def depth_input():
        edepth = int(input("Enter the engine depth (1-20): "))
        if len(edepth) == 0:
            print("Please enter a valid depth")
            InputHandler.depth_input()
        if edepth > 20 or edepth < 1:
            print("Please enter a valid depth")
            InputHandler.depth_input()
        return edepth

    @staticmethod
    def year_input():
        start_year = input("Enter the start year for analysis (e.g. 2020): ")
        if len(start_year) != 4 or (re.match(r'^([\s\d]+)$', start_year) == None):
            print("Please enter a valid start year")
            InputHandler.depth_input()
        return start_year

    @staticmethod
    def month_input():
        start_month = input("Enter the start month for analysis (e.g. 01-12): ")
        if len(start_month) != 2 or (re.match(r'^([\s\d]+)$', start_month) == None):
            print("Please enter a valid start month")
            InputHandler.depth_input()
        if start_month > 12 or start_month < 1:
            print("Please enter a valid start month")
            InputHandler.depth_input()
        return start_month

    @staticmethod
    def start_datetime(start_year: str, start_month: str):
        start_datetime = (start_year + "-" + start_month + "-01" + " 00:00:00")
        start_date = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")
        current_date = datetime.now()
        if start_date > current_date:
            start_year = InputHandler.year_input()
            start_month = InputHandler.month_input()
            InputHandler.start_datetime(start_year, start_month)
        else:
            return start_date

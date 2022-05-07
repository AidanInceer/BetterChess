import chess
import chess.engine
import chess.pgn
import extract
import logging
import os
import pandas as pd
from datetime import datetime


class ChessUser:
    def __init__(self, username, edepth, start_date):
        self.username = username
        self.edepth = edepth
        self.start_date = start_date
        self.file_paths = FileHandler(username=self.username)

    def create_logger(self):
        logging.basicConfig(
            filename=self.file_paths.loggerfile,
            format='[%(levelname)s %(module)s] %(message)s',
            level=logging.INFO, datefmt='%Y/%m/%d %I:%M:%S'
            )
        self.logger = logging.getLogger(__name__)
        return self.logger

    def create_engine(self):
        self.engine = chess.engine.SimpleEngine.popen_uci(
            self.file_paths.stockfish
            )
        return self.engine

    def run_analysis(self):
        extract.data_extract(self.username, self.file_paths.pgn_data)
        self.analyse_user()
        self.export_analysis()

    def analyse_user(self):
        all_games_data = pd.read_csv(self.file_paths.pgn_data)
        for game_num, chess_game in enumerate(all_games_data["game_data"]):
            print(game_num)
            with open(self.file_paths.temp, "w") as temp_pgn:
                temp_pgn.write(chess_game)
            game = ChessGame(self.username, self.edepth, self.start_date, self.engine)
            game.analyse_game()

    def export_analysis(self):
        print("User analysis finished")


class ChessGame(ChessUser):
    def __init__(self, username, edepth, start_date, engine):
        super().__init__(username, edepth, start_date)
        self.file_paths = FileHandler(username=self.username)
        self.engine = engine

    def init_game(self):
        self.chess_game_pgn = open(self.file_paths.temp)
        self.chess_game = chess.pgn.read_game(self.chess_game_pgn)
        return self.chess_game

    def init_board(self):
        self.board = self.chess_game.board()
        return self.board

    def analyse_game(self):
        self.init_game()
        self.init_board()
        for move_num, move in enumerate(self.chess_game.mainline_moves()):
            chess_move = ChessMove(
                self.username,
                self.edepth,
                self.start_date,
                self.engine,
                self.board,
                move_num)
            chess_move.analyse_move(move)


class ChessMove(ChessGame):
    def __init__(self, username, edepth, start_date, engine, board, move_num):
        ChessGame.__init__(self, username, edepth, start_date, engine)
        self.board = board
        self.engine = engine
        self.move_num = move_num

    def analyse_move(self, move):
        self.str_bm, self.eval_bm = self.best_move()
        self.str_ml, self.eval_ml = self.mainline_move(move)
        self.evaldiff = self.eval_diff(self.move_num, self.eval_bm, self.eval_ml)
        

    def mainline_move(self, move):
        self.str_ml = str(move)
        self.board.push_san(self.str_ml)
        eval_ml_init = self.engine.analyse(
            self.board,
            chess.engine.Limit(depth=self.edepth),
            game=object()
            )
        self.eval_ml = self.move_eval(eval_ml_init)
        return self.str_ml, self.eval_ml

    def best_move(self):
        best_move = self.engine.play(
            self.board,
            chess.engine.Limit(depth=self.edepth),
            game=object()
            )
        self.str_bm = str(best_move.move)
        self.board.push_san(self.str_bm)
        eval_bm_init = self.engine.analyse(
            self.board,
            chess.engine.Limit(depth=self.edepth),
            game=object()
            )
        self.eval_bm = self.move_eval(eval_bm_init)
        self.board.pop()
        return self.str_bm, self.eval_bm

    def move_eval(self, move):
        '''Returns the evalaution if the best move were played.'''
        get_eval = str(move['score'].white())
        if "#" in get_eval:
            get_eval = get_eval[1:]
        else:
            get_eval = get_eval
        get_eval = int(get_eval)
        return get_eval

    def eval_diff(self, move_num, eval_bm, eval_ml):
        '''Returns the eval difference between the best and mainline move.'''
        if move_num % 2 == 0:
            eval_diff = round(abs(eval_bm - eval_ml), 3)
            return eval_diff
        else:
            eval_diff = round(abs(eval_ml - eval_bm), 3)
            return eval_diff


class InputHandler:
    @staticmethod
    def get_inputs():
        username = input("Enter your username: ")
        edepth = input("Enter there engine depth: ")
        i_start_y = input("Enter the start year for analysis (e.g. 2020): ")
        i_start_m = input("Enter the start month for analysis (e.g. 01-12): ")
        i_start_datetime = (i_start_y + "-" + i_start_m + "-01" + " 00:00:00")
        start_date = datetime.strptime(i_start_datetime, "%Y-%m-%d %H:%M:%S")
        return {"username": username, "edepth": edepth, "start_date": start_date}


class FileHandler:
    def __init__(self, username):
        self.username = username
        self.dir = os.path.dirname(__file__)
        stockfish_path = r"../lib/stockfish_14.1/stockfish_14.1_win_x64_avx2.exe"
        self.stockfish = os.path.join(self.dir, stockfish_path)
        self.loggerfile = os.path.join(
            self.dir,
            rf"../logs/{self.username}_game_log.txt"
            )
        self.temp = os.path.join(self.dir, r"../data/temp.pgn")
        self.move_data = os.path.join(self.dir, r"../data/move_data.csv")
        self.game_data = os.path.join(self.dir, r"../data/game_data.csv")
        self.pgn_data = os.path.join(
            self.dir,
            rf"../data/pgn_data/{self.username}_pgn_data.csv"
            )

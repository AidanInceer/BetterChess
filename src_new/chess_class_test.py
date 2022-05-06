import chess
import chess.engine
import chess.pgn
import extract
import logging
import os
import pandas as pd
from datetime import datetime


class UserAnalysis:
    def __init__(self, username, edepth, start_date):
        self.username = username
        self.edepth = edepth
        self.start_date = start_date
        self.file_paths = FileHandler(username=self.username)
        self.create_logger()

    def create_logger(self):
        logging.basicConfig(
            filename=self.file_paths.loggerfile,
            format='[%(levelname)s %(module)s] %(message)s',
            level=logging.INFO, datefmt='%Y/%m/%d %I:%M:%S'
            )
        self.logger = logging.getLogger(__name__)
        return self.logger

    def analyse(self):
        self.init_engine()
        extract.data_extract(self.username, self.file_paths.pgn_data)
        self.data = self.parse_data()
        self.process_games()
        self.export_analysis()

    def init_engine(self):
        self.engine = chess.engine.SimpleEngine.popen_uci(
            self.file_paths.stockfish
            )
        return self.engine

    def parse_data(self):
        all_games_data = pd.read_csv(self.file_paths.pgn_data)
        for game in all_games_data["game_data"]:
            with open(self.file_paths.temp, "w") as temp_pgn:
                temp_pgn.write(game)
            chess_game_pgn = open(self.file_paths.temp)
            chess_game = chess.pgn.read_game(chess_game_pgn)
            yield chess_game

    def process_games():
        pass

    def export_analysis():
        pass


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
        self.loggerfile = os.path.join(self.dir, rf"../logs/{self.username}_game_log.txt")
        self.temp = os.path.join(self.dir, r"../data/temp.pgn")
        self.move_data = os.path.join(self.dir, r"../data/move_data.csv")
        self.game_data = os.path.join(self.dir, r"../data/game_data.csv")
        self.pgn_data = os.path.join(self.dir, rf"../data/pgn_data/{self.username}_pgn_data.csv")


class ChessGame:
    def __init__(self, game):
        self.game = 
        
    pass


class ChessMove:
    pass

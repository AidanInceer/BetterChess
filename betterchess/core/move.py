"""Module for analysing a given move of a chess game.
"""
import math
import sqlite3
from dataclasses import dataclass
from typing import Union

import chess
import chess.engine
import chess.pgn
import mysql.connector
import pandas as pd
from chess import Board
from sqlalchemy import create_engine

from betterchess.utils.handlers import EnvHandler, FileHandler, InputHandler, RunHandler


@dataclass
class Move:
    """Class for analysing a given chess move."""

    input_handler: InputHandler
    file_handler: FileHandler
    run_handler: RunHandler
    env_handler: EnvHandler
    iter_metadata: dict
    game_metadata: dict
    move_metadata: dict

    def analyse(self) -> None:
        """Method for running the move analysis."""
        self.str_bm, self.eval_bm = self.best_move(
            self.game_metadata["board"],
            self.run_handler.engine,
            self.input_handler.edepth,
        )
        self.str_ml, self.eval_ml = self.mainline_move(
            self.move_metadata["move"],
            self.game_metadata["board"],
            self.run_handler.engine,
            self.input_handler.edepth,
        )
        self.evaldiff = self.eval_delta(
            self.move_metadata["move_num"], self.eval_bm, self.eval_ml
        )
        self.move_acc = self.move_accuracy(self.evaldiff)
        self.move_type = self.assign_move_type(self.move_acc)
        self.square_int = self.get_piece_square_int(self.move_metadata["move"])
        self.curr_board = self.get_curr_board()
        self.piece = self.chess_piece(self.curr_board, self.square_int)
        self.move_col = self.move_colour(self.move_metadata["move_num"])
        self.castle_type = self.castling_type(self.piece, self.move_col, self.str_ml)
        self.w_castle_mv_num = self.white_castle_move_num(
            self.castle_type, self.move_metadata["move_num"]
        )
        self.b_castle_mv_num = self.black_castle_move_num(
            self.castle_type, self.move_metadata["move_num"]
        )
        self.timers = self.filter_timecont_header(self.file_handler.path_temp)
        self.move_time = self.get_time_spent_on_move(
            self.file_handler.path_temp, self.move_metadata["move_num"], self.timers
        )
        self.move_df = self.create_move_df()
        self.export_move_data(self.move_df, self.env_handler)
        self.append_to_game_lists()

    def create_move_df(self) -> pd.DataFrame:
        """Create the move dataframe.

        Returns:
            pd.DataFrame: Move dataframe.
        """
        self.move_df = pd.DataFrame(
            {
                "Username": self.input_handler.username,
                "Game_date": self.game_metadata["game_datetime"],
                "Engine_depth": self.input_handler.edepth,
                "Game_number": self.iter_metadata["game_num"],
                "Move_number": self.move_metadata["move_num"],
                "Move": self.str_ml,
                "Move_eval": self.eval_ml,
                "Best_move": self.str_bm,
                "Best_move_eval": self.eval_bm,
                "Move_eval_diff": self.evaldiff,
                "Move_accuracy": self.move_acc,
                "Move_type": self.move_type,
                "Piece": self.piece,
                "Move_colour": self.move_col,
                "Castling_type": self.castle_type,
                "White_castle_num": self.w_castle_mv_num,
                "Black_castle_num": self.b_castle_mv_num,
                "Move_time": self.move_time,
            },
            index=[0],
        )
        return self.move_df

    def mainline_move(
        self,
        move: chess.Move,
        board: Board,
        engine: chess.engine.SimpleEngine,
        edepth: int,
    ) -> tuple:
        """Analysis of the actual chess move played - returns the evaluation.

        Args:
            move (chess.Move): Move.
            board (Board): Current game board.
            engine (chess.engine.SimpleEngine): Engine for analysis.

        Returns:
            tuple: Move string and Move evaluation.
        """
        str_ml = str(move)
        board.push_san(san=str_ml)
        eval_ml_init = engine.analyse(
            board=board,
            limit=chess.engine.Limit(depth=edepth),
            game=object(),
        )
        eval_ml = self.move_eval(move=eval_ml_init)
        return str_ml, eval_ml

    def best_move(
        self, board: Board, engine: chess.engine.SimpleEngine, edepth: int
    ) -> tuple:
        """Analysis of the best chess move played - returns the evaluation.

        Args:
            board (Board): Current game board.
            engine (chess.engine.SimpleEngine): Engine for analysis.

        Returns:
            tuple: Best move string and best move evaluation.
        """
        best_move = engine.play(
            board=board,
            limit=chess.engine.Limit(depth=edepth),
            game=object(),
        )
        str_bm = str(best_move.move)
        board.push_san(san=str_bm)
        eval_bm_init = engine.analyse(
            board=board,
            limit=chess.engine.Limit(depth=edepth),
            game=object(),
        )
        eval_bm = self.move_eval(move=eval_bm_init)
        board.pop()
        return str_bm, eval_bm

    @staticmethod
    def move_eval(move: chess.Move) -> int:
        """Filters the evaluation to remove checkmate and converts to int.

        Args:
            move (chess.Move): A chess move.

        Returns:
            get_eval (int): Integer of the move eval.
        """
        get_eval = str(move["score"].white())
        if "#" in get_eval:
            get_eval = get_eval[1:]
        get_eval = int(get_eval)
        return get_eval

    @staticmethod
    def eval_delta(move_num: int, eval_bm: float, eval_ml: float) -> float:
        """Different between best move and mainline move.

        Args:
            move_num (int): Move number.
            eval_bm (float): Best move evaluation.
            eval_ml (float): Mainline move evaluation.

        Returns:
            eval_diff (float): Different between main and best move.
        """
        if move_num % 2 == 0:
            eval_diff = round(abs(eval_bm - eval_ml), 3)
            return eval_diff
        else:
            eval_diff = round(abs(eval_ml - eval_bm), 3)
            return eval_diff

    @staticmethod
    def move_accuracy(eval_diff: float) -> float:
        """Move accuracy calulation through inverse sigmoid function.

        Args:
            eval_diff (float): Different between main and best move.

        Returns:
            move_acc (float): Returns an accuracy between 0-100.
        """
        m, v = 0, 1.5
        move_acc = round(math.exp(-0.00003 * ((eval_diff - m) / v) ** 2) * 100, 1)
        return move_acc

    @staticmethod
    def assign_move_type(move_acc: float) -> int:
        """Calculate the move type of a move.

        Args:
            move_acc (_type_): Accuracy between 0-100.

        Returns:
            int: Type of move
                - best = 2,
                - excellent = 1,
                - good = 0,
                - inacc = -1,
                - mistake = -2,
                - blunder = -3,
                - missed win = -4
        """
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
    def chess_piece(curr_board: chess.BaseBoard, square_int: int) -> str:
        """Gets the piece type that was just moved.

        Args:
            curr_board (chess.BaseBoard): Current board position after move was played.
            square_int (int): Square number (0-63).

        Returns:
            str: Chess piece.
        """
        piece_type_num = chess.BaseBoard.piece_type_at(curr_board, square=square_int)
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
        """Gets the current board position.

        Returns:
            chess.BaseBoard: Current board position.
        """
        curr_fen = self.game_metadata["board"].board_fen()
        curr_board = chess.BaseBoard(board_fen=curr_fen)
        return curr_board

    @staticmethod
    def get_piece_square_int(move) -> int:
        """Returns the square int value that the piece just moved is in.

        Args:
            move (chess.Move): Chess move.

        Returns:
            int: 0-63.
        """
        piece_col = str(move)[2:3]
        piece_row = str(move)[3:4]
        piece_square = str(piece_col + piece_row)
        square_int = chess.parse_square(name=piece_square)
        return square_int

    @staticmethod
    def move_colour(move_num) -> str:
        """Gets the move colour.

        Args:
            move_num (int): Move number.

        Returns:
            str: black or white.
        """
        if move_num % 2 == 0:
            mv_colour = "white"
        else:
            mv_colour = "black"
        return mv_colour

    @staticmethod
    def castling_type(piece: str, move_col: str, str_ml: str) -> str:
        """Determines whether a played castled long, short or not at all.

        Args:
            piece (str): Chess Piece.
            move_col (str): Move colour.
            str_ml (str): Mainline move string.

        Returns:
            str: Castling type by colour.
        """
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
    def white_castle_move_num(castle_type: Union[str, None], move_num: int) -> int:
        """Which move white castle on.

        Args:
            castle_type (str): Castle type.
            move_num (int): Move number.

        Returns:
            int: Castling move number.
        """
        if castle_type == "white_short" or castle_type == "white_long":
            white_castle_move = move_num
        else:
            white_castle_move = 0
        return white_castle_move

    @staticmethod
    def black_castle_move_num(castle_type: Union[str, None], move_num: int) -> int:
        """Which move black castle on.

        Args:
            castle_type (str): Castle type.
            move_num (int): Move numbe

        Returns:
            int:  Castling move number.
        """
        if castle_type == "black_short" or castle_type == "black_long":
            black_castle_move = move_num
        else:
            black_castle_move = 0
        return black_castle_move

    @staticmethod
    def get_time_spent_on_move(path_temp: str, move_num: int, timers: tuple) -> float:
        """Gets the time spent on a given move in seconds.

        Args:
            path_temp (str): Pgn filepath for current game.
            move_num (int): Move number.
            timers (tuple): Time control and time interval of the current game.

        Returns:
            float: Seconds to make a move.
        """
        chess_game_pgn = open(file=path_temp)
        game = chess.pgn.read_game(handle=chess_game_pgn)
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
    def filter_timecont_header(path_temp: str) -> tuple[float, float, int]:
        """Filters the time control header to determine the starting time of a game.

        Args:
            path_temp (str): Pgn filepath for current game.

        Returns:
            tuple[float, float, int]: Time control and time interval of the current game.
        """
        chess_game_pgn = open(file=path_temp)
        game = chess.pgn.read_game(handle=chess_game_pgn)
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

    def export_move_data(self, move_df: pd.DataFrame, env_handler: EnvHandler) -> None:
        """Exports the move dataframe to sql database.

        Args:
            move_df (pd.DataFrame): Move dataframe.
        """
        if env_handler.db_type == "mysql":
            conn = mysql.connector.connect(
                host=env_handler.mysql_host,
                user=env_handler.mysql_user,
                database=env_handler.mysql_db,
                password=env_handler.mysql_password,
            )
            mysql_engine = create_engine(
                f"{self.env_handler.mysql_driver}://{self.env_handler.mysql_user}:{self.env_handler.mysql_password}@{self.env_handler.mysql_host}/{self.env_handler.mysql_db}"
            )
            move_df.to_sql("move_data", mysql_engine, if_exists="append", index=False)
            conn.commit()
            conn.close()
        elif env_handler.db_type == "sqlite":
            conn = sqlite3.connect(
                FileHandler(self.input_handler.username).path_database
            )
            move_df.to_sql("move_data", conn, if_exists="append", index=False)
            conn.commit()
            conn.close()

    def append_to_game_lists(self) -> None:
        """Appends the move data to the games lists so it can be accessed by the Game class."""
        self.game_metadata["game_lists_dict"]["gm_mv_num"].append(
            self.move_metadata["move_num"]
        )
        self.game_metadata["game_lists_dict"]["gm_mv"].append(self.str_ml)
        self.game_metadata["game_lists_dict"]["gm_best_mv"].append(self.str_bm)
        self.game_metadata["game_lists_dict"]["best_move_eval"].append(self.eval_bm)
        self.game_metadata["game_lists_dict"]["mainline_eval"].append(self.eval_ml)
        self.game_metadata["game_lists_dict"]["move_eval_diff"].append(self.evaldiff)
        self.game_metadata["game_lists_dict"]["gm_mv_ac"].append(self.move_acc)
        self.game_metadata["game_lists_dict"]["move_type_list"].append(self.move_type)
        self.game_metadata["game_lists_dict"]["w_castle_num"].append(
            self.w_castle_mv_num
        )
        self.game_metadata["game_lists_dict"]["b_castle_num"].append(
            self.b_castle_mv_num
        )

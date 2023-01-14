"""_summary_
"""
import sqlite3
import time
from dataclasses import dataclass
from datetime import date, datetime

import chess
import chess.engine
import chess.pgn
import numpy as np
import pandas as pd

from betterchess.core.headers import Headers
from betterchess.core.move import Move
from betterchess.utils.handlers import FileHandler, InputHandler, RunHandler
from betterchess.utils.progress import Progress


@dataclass
class Game:
    """Functions and data relating to analysing a chess game."""

    input_handler: InputHandler
    file_handler: FileHandler
    run_handler: RunHandler
    iter_metadata: dict

    def run_game_analysis(self) -> None:
        """Sets up a game and runs the analysis for a game."""
        log_dt = Prepare.all_games(Prepare, self.file_handler.path_userlogfile)
        self.game_metadata = Prepare.current_game_analysis(
            Prepare,
            self.input_handler,
            self.file_handler,
            self.run_handler,
            self.iter_metadata,
        )
        if (
            self.game_metadata["game_datetime"] >= log_dt
            and self.game_metadata["game_datetime"] >= self.input_handler.start_date
        ):
            start_time = time.perf_counter()
            self.run_handler.logger.info(
                f'| {self.input_handler.username} | {self.game_metadata["game_datetime"]} | {self.iter_metadata["game_num"]}'
            )
            for move_num, move in enumerate(
                self.game_metadata["chess_game"].mainline_moves()
            ):
                move_metadata = {"move": move, "move_num": move_num}
                chess_move = Move(
                    self.input_handler,
                    self.file_handler,
                    self.run_handler,
                    self.iter_metadata,
                    self.game_metadata,
                    move_metadata,
                )
                chess_move.analyse()
                del chess_move
            try:
                total_moves = move_num
            except UnboundLocalError:
                total_moves = 0
            self.analyse_game(
                self.game_metadata["game_lists_dict"]["move_type_list"], total_moves
            )
            end_time = time.perf_counter()
            Progress.bar(
                Progress,
                self.iter_metadata["game_num"],
                self.iter_metadata["tot_games"],
                start_time,
                end_time,
            )

    def analyse_game(self, move_type_list: dict, total_moves: int) -> None:
        """Consolidates game analysis data and exports it to db.

        Args:
            move_type_list (dict): List of move types e.g. no. blunders.
            total_moves (int): Total number of moves in a game.
        """
        move_dict = self.sum_move_types(move_type_list)
        game_df = self.user_game_data(
            move_dict,
            self.game_metadata["game_datetime"],
            self.game_metadata["game_lists_dict"]["gm_mv_ac"],
            self.game_metadata["game_lists_dict"]["w_castle_num"],
            self.game_metadata["game_lists_dict"]["b_castle_num"],
            total_moves,
            self.game_metadata["headers"],
            self.input_handler.username,
            self.input_handler.edepth,
            self.iter_metadata["game_num"],
        )
        self.export_game_data(game_df)

    def sum_move_types(self, move_type_list: list) -> dict:
        """Calculated the number of a specific type of moves for black and
        white in a chess game.

        Args:
            move_type_list (list): List of move types.

        Returns:
            dict: Dictionary of moves type lists.
        """
        move_dict = {
            "Num_w_best": move_type_list[::2].count(2),
            "Num_b_best": move_type_list[1::2].count(2),
            "Num_w_excl": move_type_list[::2].count(1),
            "Num_b_excl": move_type_list[1::2].count(1),
            "Num_w_good": move_type_list[::2].count(0),
            "Num_b_good": move_type_list[1::2].count(0),
            "Num_w_inac": move_type_list[::2].count(-1),
            "Num_b_inac": move_type_list[1::2].count(-1),
            "Num_w_mist": move_type_list[::2].count(-2),
            "Num_b_mist": move_type_list[1::2].count(-2),
            "Num_w_blun": move_type_list[::2].count(-3),
            "Num_b_blun": move_type_list[1::2].count(-3),
            "Num_w_misw": move_type_list[::2].count(-4),
            "Num_b_misw": move_type_list[1::2].count(-4),
        }
        return move_dict

    def user_game_data(
        self,
        move_dict: dict,
        game_datetime: str,
        game_move_acc: list,
        w_castle_num: list,
        b_castle_num: list,
        total_moves: int,
        headers: dict,
        username: str,
        edepth: int,
        game_num: int,
    ) -> pd.DataFrame:
        """Creates the game data dataframe.

        Args:
            move_dict (dict):  Dictionary of moves type lists.
            game_datetime (str): Datetime of the game.
            game_move_acc (list): List of move accuracies.
            w_castle_num (list): Point at which white castles.
            b_castle_num (list): Point at which black castles.
            total_moves (int): Total number of moves.
            headers (dict): Game header dictionary.
            username (str): Username.
            edepth (int): Engine depth.
            game_num (int): Game number of user.

        Returns:
            pd.DataFrame: dataframe of game data.
        """

        self.time_of_day = self.game_time_of_day(game_datetime)
        self.day_of_week = self.game_day_of_week(game_datetime)
        self.game_pgn = self.get_curr_game_pgn(
            game_num, username, self.file_handler.path_temp
        )

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
            self.user_win_percent = self.get_predicted_win_percentage(
                headers["White_rating"], headers["Black_rating"]
            )
            self.opp_win_percent = self.get_predicted_win_percentage(
                headers["Black_rating"], headers["White_rating"]
            )
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
            self.user_castle_phase = self.black_castle_phase(b_castle_num, total_moves)
            self.opp_castle_phase = self.white_castle_phase(w_castle_num, total_moves)
            self.user_win_percent = self.get_predicted_win_percentage(
                headers["Black_rating"], headers["White_rating"]
            )
            self.opp_win_percent = self.get_predicted_win_percentage(
                headers["White_rating"], headers["Black_rating"]
            )
        game_df = pd.DataFrame(
            {
                "Username": username,
                "Game_date": game_datetime,
                "Game_time_of_day": self.time_of_day,
                "Game_weekday": self.day_of_week,
                "Engine_depth": edepth,
                "Game_number": game_num,
                "Game_type": headers["Time_control"],
                "White_player": headers["White_player"],
                "White_rating": headers["White_rating"],
                "Black_player": headers["Black_player"],
                "Black_rating": headers["Black_rating"],
                "User_colour": headers["User_Colour"],
                "User_rating": headers["User_rating"],
                "Opponent_rating": headers["Opponent_rating"],
                "User_win_percent": self.user_win_percent,
                "Opp_win_percent": self.opp_win_percent,
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
                "Game_pgn": self.game_pgn,
            },
            index=[0],
        )
        return game_df

    def export_game_data(self, game_df: pd.DataFrame):
        """Exports game data to sql.

        Args:
            game_df (pd.Dataframe): dataframe of game data
        """
        conn = sqlite3.connect(FileHandler(self.input_handler.username).path_database)
        game_df.to_sql("game_data", conn, if_exists="append", index=False)
        conn.commit()
        conn.close()

    @staticmethod
    def game_time_of_day(game_datetime: datetime) -> str:
        """Returns the time segment of the day.

        Args:
            game_datetime (datetime): Datetime of the game.

        Returns:
            str: Game time section e.g. Morning/Evening.
        """
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
    def game_day_of_week(game_datetime: datetime) -> str:
        """Returns the weekday which the game was played.

        Args:
            game_datetime (datetime): Datetime of the game.

        Returns:
            str: Day of the week.
        """
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
        """game accuracy of white player (Out of 100).

        Args:
            game_move_acc (list): Game accuracy list.

        Returns:
            float: Game accuracy of white player.
        """
        w_list = game_move_acc[::2]
        list_len = len(game_move_acc[::2])
        if list_len == 0:
            wg_acc = 0
        else:
            wg_acc = round(sum(w_list) / list_len, 2)
        return wg_acc

    @staticmethod
    def game_b_acc(game_move_acc: list) -> float:
        """game accuracy of black player (Out of 100).

        Args:
            game_move_acc (list): Game accuracy list.

        Returns:
            float: Game accuracy of black player.
        """
        b__list = game_move_acc[1::2]
        list_len = len(game_move_acc[1::2])
        if list_len == 0:
            bg_acc = 0
        else:
            bg_acc = round(sum(b__list) / list_len, 2)
        return bg_acc

    @staticmethod
    def op_w_acc(game_move_acc: list) -> float:
        """Opening game accuracy for white.

        Args:
            game_move_acc (list):  Game accuracy list.

        Returns:
            float: Opening accuracy of white player.
        """
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
        """Midgame accuracy for white.

        Args:
            game_move_acc (list):  Game accuracy list.

        Returns:
            float: Midgame accuracy of white player.
        """
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
        """Endgame accuracy for white.

        Args:
            game_move_acc (list):  Game accuracy list.

        Returns:
            float: Endgame accuracy of white player.
        """
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
        """Opening accuracy for black.

        Args:
            game_move_acc (list):  Game accuracy list.

        Returns:
            float: Opening accuracy of black player.
        """
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
        """Midgame accuracy for black.

        Args:
            game_move_acc (list):  Game accuracy list.

        Returns:
            float: Midgame accuracy of black player.
        """
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
        """Endgame accuracy for black.

        Args:
            game_move_acc (list):  Game accuracy list.

        Returns:
            float: Endgame accuracy of black player.
        """
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
        """Whites area of lowest accuracy.

        Args:
            ow (float): Opening accuracy.
            mw (float): Midgame accuracy.
            ew (float): Endgame accuracy.

        Returns:
            str: Game section.
        """
        if ow < ew and ow < mw:
            white_sector_improvement = "Opening"
        elif mw < ow and mw < ew:
            white_sector_improvement = "Midgame"
        else:
            white_sector_improvement = "Endgame"
        return white_sector_improvement

    @staticmethod
    def b_sec_imp(ob: float, mb: float, eb: float) -> str:
        """Black area of lowest accuracy

        Args:
            ow (float): Opening accuracy.
            mw (float): Midgame accuracy.
            ew (float): Endgame accuracy.

        Returns:
            str: Game section.
        """
        if ob < mb and ob < eb:
            black_sector_improvement = "Opening"
        elif mb < ob and mb < eb:
            black_sector_improvement = "Midgame"
        else:
            black_sector_improvement = "Endgame"
        return black_sector_improvement

    @staticmethod
    def white_castle_move_num(white_castle_num: list) -> int:
        """Whites castling move

        Args:
            white_castle_num (int): Castling move.

        Returns:
            int: Move number of white that white castled.
        """
        return sum(white_castle_num)

    @staticmethod
    def black_castle_move_num(black_castle_num: list) -> int:
        """Black castling move

        Args:
            black_castle_num (int): Castling move.

        Returns:
            int: Move number of black that black castled.
        """
        return sum(black_castle_num)

    @staticmethod
    def has_white_castled(white_castle_num: list) -> int:
        """Checks to see if white has castled.

        Args:
            white_castle_num (list): Castling move list.

        Returns:
            int: 1 if castled 0 if not castled.
        """
        if sum(white_castle_num) > 0:
            return 1
        else:
            return 0

    @staticmethod
    def has_black_castled(black_castle_num: list) -> int:
        """Checks to see if black has castled.

        Args:
            black_castle_num (list): Castling move list.

        Returns:
            int: 1 if castled 0 if not castled.
        """
        if sum(black_castle_num) > 0:
            return 1
        else:
            return 0

    @staticmethod
    def white_castle_phase(white_castle_num: list, total_moves: int) -> str:
        """Game section which white castled.

        Args:
            white_castle_num (list):  Castling move list.
            total_moves (int): Total number of moves

        Returns:
            str: Game section.
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
        """Game section which black castled.

        Args:
            black_castle_num (list):  Castling move list.
            total_moves (int): Total number of moves.

        Returns:
            str: Game section.
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

    @staticmethod
    def get_predicted_win_percentage(player_1: int, player_2: int) -> float:
        """Predicted win percentage of a user before the game has been played.

        Args:
            player_1 (int): player 1.
            player_2 (int): player 2.

        Returns:
            float: Predicted win percentage.
        """
        exp_term = (player_2 - player_1) / 400
        pred_win_percent = round((1 / (1 + 10**exp_term)) * 100, 2)
        return pred_win_percent

    @staticmethod
    def get_curr_game_pgn(game_num: int, username: str, path_temp: str) -> pd.DataFrame:
        """Gets the current games pgn string for use in webapp.

        Args:
            game_num (int): Game number of the current game.
            path_database (str): Path to database.
            username (str): Username.

        Returns:
            (pd.DataFrame): Dataframe of the current game
        """
        with open(path_temp, "r") as pgn_game_file:
            pgn_game_file = pgn_game_file.readlines()
        return str(pgn_game_file)


@dataclass
class Prepare:
    """Class to prepare games/data/runs relating to the Game class."""

    def current_game_analysis(
        self,
        input_handler: InputHandler,
        file_handler: FileHandler,
        run_handler: RunHandler,
        iter_metadata: dict,
    ) -> dict:
        """Prepares the current game for analysis.

        Args:
            input_handler (InputHandler): InputHandler info.
            file_handler (FileHandler): FileHandler info.
            run_handler (RunHandler): RunHandler info.
            iter_metadata (dict): iteration metadata.

        Returns:
            dict: _description_
        """
        chess_game = self.init_game(self, file_handler.path_temp)
        board = self.init_board(self, chess_game)
        game_lists_dict = self.init_game_lists(self)
        game_headers = Headers(
            input_handler, file_handler, run_handler, iter_metadata, chess_game
        )
        headers = game_headers.collect()
        game_metadata = {
            "headers": headers,
            "game_datetime": headers["Game_datetime"],
            "board": board,
            "chess_game": chess_game,
            "game_lists_dict": game_lists_dict,
        }
        return game_metadata

    def init_game(self, path_temp: str) -> chess.pgn.Game:
        """Initialzies the current temporary game.

        Args:
            path_temp (str): Path of the temporary pgn file.

        Returns:
            chess.pgn.Game: Current chess game.
        """
        chess_game_pgn = open(path_temp)
        return chess.pgn.read_game(chess_game_pgn)

    def init_board(self, chess_game: chess.pgn.Game) -> chess.Board:
        """Initialzies the current temporary games board.

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            chess.Board: Current chess board.
        """
        return chess_game.board()

    def init_game_lists(self) -> dict:
        """Empty Games lists for the current game.

        Returns:
            dict: Dictionary of empty game lists.
        """
        game_lists_dict = {
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
        return game_lists_dict

    def all_games(self, path_userlogfile: str) -> datetime:
        """Wrapper for get_last_logged_game function to improve code flow.

        Args:
            path_userlogfile (str): User log file.

        Returns:
            datetime: Datetime of last logged game.
        """
        return self.get_last_logged_game(self, path_userlogfile)

    def get_last_logged_game(self, path_userlogfile: str) -> datetime:
        """Returns the last logged game date.

        Args:
            path_userlogfile (str): User log file.

        Returns:
            datetime:  Datetime of last logged game.
        """
        game_log_list = self.get_game_log_list(self, path_userlogfile)
        llog = game_log_list[-1]
        llog_date_str = llog.split("|")[2].strip()
        llog_date = datetime.strptime(llog_date_str, "%Y-%m-%d %H:%M:%S")
        return llog_date

    def get_game_log_list(self, path_userlogfile: str) -> list:
        """Collects the log list.

        Args:
            path_userlogfile (str): User log file.

        Returns:
            list: List of logged games analysed.
        """
        game_log_list = []
        with open(path_userlogfile, mode="r") as log_file:
            lines = log_file.readlines()
            self.logfile_line_checker_multi(self, game_log_list, lines)
        return game_log_list

    def logfile_line_checker_multi(self, game_log_list: list, lines: list[str]) -> None:
        """Filter for log list to remove lines not relating to the user/game module.

        Args:
            game_log_list (list): List of log lines
            lines (list[str]): Lines withing the log file.
        """
        for line in lines:
            if ("user" in line) or ("game" in line):
                game_log_list.append(line)

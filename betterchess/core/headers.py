"""Module for creating/parsing the headers within a given pgn chess game file.
"""
from dataclasses import dataclass
from datetime import datetime

import chess
import chess.engine
import chess.pgn

from betterchess.utils.handlers import FileHandler, InputHandler, RunHandler


@dataclass
class Headers:
    """Class for parsing and collecting a chess.coms game headers."""

    input_handler: InputHandler
    file_handler: FileHandler
    run_handler: RunHandler
    iter_metadata: dict
    chess_game: chess.pgn.Game

    def collect(self):
        """Collects the dictionary of chess game headers.

        Returns:
            header_dict (dict): Dictionary of header information.
        """
        self.calculate_headers()
        return self.create_header_dict()

    def calculate_headers(self):
        """Main function for creating instance variables and running methods."""
        self.username = self.input_handler.username
        self.engine = self.run_handler.engine
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

    def create_header_dict(self) -> dict:
        """Creates the dictionary of a games header information.

        Returns:
            header_dict (dict): Dictionary of header information.
        """
        return {
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

    def time_control(self, chess_game: chess.pgn.Game) -> str:
        """Gets the time control header from the chess game pgn.

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            str: Time control.
        """
        return chess_game.headers["TimeControl"]

    def player_white(self, chess_game: chess.pgn.Game) -> str:
        """Gets the white players username header from the chess game pgn.

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            str: White player username.
        """
        return chess_game.headers["White"]

    def player_black(self, chess_game: chess.pgn.Game) -> str:
        """Gets the black players username header from the chess game pgn.

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            str: Black player username.
        """
        return chess_game.headers["Black"]

    def user_colour(self, white: str, username: str) -> str:
        """Gets the players colour header from the chess game pgn.

        Args:
            white (str): White players username.
            username (str): Username.

        Returns:
            str: Users colour.
        """
        return "White" if white == username else "Black"

    def rating_white(self, chess_game: chess.pgn.Game) -> int:
        """Gets whites rating header from the chess game pgn.

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            int: Whites player rating.
        """
        return int(chess_game.headers["WhiteElo"])

    def rating_black(self, chess_game: chess.pgn.Game) -> int:
        """Gets blacks rating header from the chess game pgn.

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            int: Blacks player rating.
        """
        return int(chess_game.headers["BlackElo"])

    def opening_cls(self, chess_game: chess.pgn.Game) -> str:
        """Gets the opening classification for the current chess game.

        Args:
            chess_game (chess.pgn.Game):  Current chess game.

        Returns:
            str: Opening classification.
        """
        try:
            opening_class = chess_game.headers["ECO"]
        except KeyError:
            opening_class = "000"
        return opening_class

    def opening_nm(self, chess_game: chess.pgn.Game) -> str:
        """Gets the opening name for the current chess game.

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            str: Opening name.
        """
        try:
            opening_name_raw = chess_game.headers["ECOUrl"]
        except KeyError:
            opening_name_raw = "/NA"
        opening_string = opening_name_raw.split("/")[-1]
        return str(opening_string.replace("-", " ").strip())

    def game_termination(self, chess_game: chess.pgn.Game, username: str) -> str:
        """How the current chess game ended e.g. draw by...

        Args:
            chess_game (chess.pgn.Game): Current chess game.
            username (str): Username

        Returns:
            termination (str): How the game ended.
        """
        termination_raw = chess_game.headers["Termination"]
        winner_check = termination_raw.split(" ")
        draw_check = " ".join(winner_check[:2])
        if winner_check[0] == username:
            return "Win " + " ".join(winner_check[2:])
        elif draw_check == "Game drawn":
            return "Draw " + " ".join(winner_check[2:])
        else:
            return "Loss " + " ".join(winner_check[2:])

    def rating_user(self, player: str, rating_w: int, rating_b: int) -> int:
        """Gets the users chess rating for the current game type.

        Args:
            player (str): A given players username.
            rating_w (int): White rating.
            rating_b (int): Black rating.

        Returns:
           user_rating (int): Players rating.
        """
        return rating_w if player == "White" else rating_b

    def rating_opponent(self, player: str, rating_w: int, rating_b: int) -> int:
        """Gets the opponents chess rating for the current game type.

        Args:
            player (str): A given players username.
            rating_w (int): White rating.
            rating_b (int): Black rating.

        Returns:
           user_rating (int): Opponents rating.
        """
        return rating_b if player == "White" else rating_w

    def win_draw_loss(self, chess_game: chess.pgn.Game) -> str:
        """Gets the result of the game (Win/Draw/Loss).

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            str: Win/Draw/Loss
        """
        if chess_game.headers["Result"] == "1-0":
            return "White"
        elif chess_game.headers["Result"] == "0-1":
            return "Black"
        else:
            return "Draw"

    def user_winr(self, winner: str, player: str) -> str:
        """Returns whether the player won/drew/lost the game.

        Args:
            winner (str): Either `White` or `Black`.
            player (str): Players username.

        Returns:
            str: Win/Draw/Loss
        """
        pww = winner == "White" and player == "White"
        pbw = winner == "Black" and player == "Black"
        pwl = winner == "Black" and player == "White"
        pbl = winner == "White" and player == "Black"
        if pww or pbw:
            return "Win"
        elif pwl or pbl:
            return "Loss"
        else:
            return "Draw"

    def game_dt(self, chess_game: chess.pgn.Game) -> str:
        """Date of the game.

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            str: Game date.
        """
        return chess_game.headers["UTCDate"]

    def game_t(self, chess_game: chess.pgn.Game) -> str:
        """Time of the game.

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            str: Game Time.
        """
        return chess_game.headers["UTCTime"]

    def game_dt_time(self, game_date: str, game_time: str) -> datetime:
        """Returns the game datetime of the current chess game.

        Args:
            game_date (str): Game date.
            game_time (str): Game Time.

        Returns:
            datetime: datetime of the current chess game.
        """
        game_date_time = f"{game_date} {game_time}"
        return datetime.strptime(game_date_time, "%Y.%m.%d %H:%M:%S")

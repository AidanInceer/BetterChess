"""_summary_
"""
from betterchess.utils.handlers import InputHandler, FileHandler, RunHandler
from dataclasses import dataclass
from datetime import datetime
import chess
import chess.engine
import chess.pgn


@dataclass
class Headers:
    """_summary_

    Returns:
        _type_: _description_
    """
    input_handler: InputHandler
    file_handler: FileHandler
    run_handler: RunHandler
    iter_metadata: dict
    chess_game: chess.pgn.Game

    def collect(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        self.calculate_headers()
        header_dict = self.create_header_dict()
        return header_dict

    def calculate_headers(self):
        """_summary_
        """
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
        """_summary_

        Returns:
            dict: _description_
        """
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

    def time_control(self, chess_game: chess.pgn.Game) -> str:
        """_summary_

        Args:
            chess_game (chess.pgn.Game): _description_

        Returns:
            str: _description_
        """
        time_cont = chess_game.headers["TimeControl"]
        return time_cont

    def player_white(self, chess_game: chess.pgn.Game) -> str:
        """_summary_

        Args:
            chess_game (chess.pgn.Game): _description_

        Returns:
            str: _description_
        """
        white = chess_game.headers["White"]
        return white

    def player_black(self, chess_game: chess.pgn.Game) -> str:
        """_summary_

        Args:
            chess_game (chess.pgn.Game): _description_

        Returns:
            str: _description_
        """
        black = chess_game.headers["Black"]
        return black

    def user_colour(self, white: str, username: str) -> str:
        """_summary_

        Args:
            white (str): _description_
            username (str): _description_

        Returns:
            str: _description_
        """
        player = "White" if white == username else "Black"
        return player

    def rating_white(self, chess_game: chess.pgn.Game) -> int:
        """_summary_

        Args:
            chess_game (chess.pgn.Game): _description_

        Returns:
            int: _description_
        """
        ratingwhite = int(chess_game.headers["WhiteElo"])
        return ratingwhite

    def rating_black(self, chess_game: chess.pgn.Game) -> int:
        """_summary_

        Args:
            chess_game (chess.pgn.Game): _description_

        Returns:
            int: _description_
        """
        ratingblack = int(chess_game.headers["BlackElo"])
        return ratingblack

    def opening_cls(self, chess_game: chess.pgn.Game) -> str:
        """_summary_

        Args:
            chess_game (chess.pgn.Game): _description_

        Returns:
            str: _description_
        """
        try:
            opening_class = chess_game.headers["ECO"]
        except KeyError:
            opening_class = "000"
        return opening_class

    def opening_nm(self, chess_game: chess.pgn.Game) -> str:
        """_summary_

        Args:
            chess_game (chess.pgn.Game): _description_

        Returns:
            str: _description_
        """
        try:
            opening_name_raw = chess_game.headers["ECOUrl"]
        except KeyError:
            opening_name_raw = "/NA"
        opening_string = opening_name_raw.split("/")[-1]
        opening_name = str(opening_string.replace("-", " ").strip())
        return opening_name

    def game_termination(self, chess_game: chess.pgn.Game, username) -> str:
        """_summary_

        Args:
            chess_game (chess.pgn.Game): _description_
            username (_type_): _description_

        Returns:
            str: _description_
        """
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

    def rating_user(self, player: str, rating_w: int, rating_b: int) -> int:
        """_summary_

        Args:
            player (str): _description_
            rating_w (int): _description_
            rating_b (int): _description_

        Returns:
            int: _description_
        """
        user_rating = rating_w if player == "White" else rating_b
        return user_rating

    def rating_opponent(self, player: str, rating_w: int, rating_b: int) -> int:
        """_summary_

        Args:
            player (str): _description_
            rating_w (int): _description_
            rating_b (int): _description_

        Returns:
            int: _description_
        """
        opp_rating = rating_b if player == "White" else rating_w
        return opp_rating

    def win_draw_loss(self, chess_game: chess.pgn.Game) -> str:
        """_summary_

        Args:
            chess_game (chess.pgn.Game): _description_

        Returns:
            str: _description_
        """
        if chess_game.headers["Result"] == "1-0":
            end_type = "White"
        elif chess_game.headers["Result"] == "0-1":
            end_type = "Black"
        else:
            end_type = "Draw"
        return end_type

    def user_winr(self, winner: str, player: str) -> str:
        """_summary_

        Args:
            winner (str): _description_
            player (str): _description_

        Returns:
            str: _description_
        """
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

    def game_dt(self, chess_game: chess.pgn.Game) -> str:
        """_summary_

        Args:
            chess_game (chess.pgn.Game): _description_

        Returns:
            str: _description_
        """
        game_date = chess_game.headers["UTCDate"]
        return game_date

    def game_t(self, chess_game: chess.pgn.Game) -> str:
        """_summary_

        Args:
            chess_game (chess.pgn.Game): _description_

        Returns:
            str: _description_
        """
        game_time = chess_game.headers["UTCTime"]
        return game_time

    def game_dt_time(self, game_date: str, game_time: str) -> datetime:
        """_summary_

        Args:
            game_date (str): _description_
            game_time (str): _description_

        Returns:
            datetime: _description_
        """
        game_date_time = f"{game_date} {game_time}"
        game_datetime = datetime.strptime(game_date_time, "%Y.%m.%d %H:%M:%S")
        return game_datetime

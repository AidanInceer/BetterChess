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
    """Class for parsing and collecting a chess.coms game headers.
    """

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
        header_dict = self.create_header_dict()
        return header_dict

    def calculate_headers(self):
        """Main function for creating instance variables and running methods.
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
        """Creates the dictionary of a games header information.

        Returns:
            header_dict (dict): Dictionary of header information.
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
        """Gets the time control header from the chess game pgn.

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            str: Time control.
        """
        time_cont = chess_game.headers["TimeControl"]
        return time_cont

    def player_white(self, chess_game: chess.pgn.Game) -> str:
        """Gets the white players username header from the chess game pgn.

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            str: White player username.
        """
        white = chess_game.headers["White"]
        return white

    def player_black(self, chess_game: chess.pgn.Game) -> str:
        """Gets the black players username header from the chess game pgn.

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            str: Black player username.
        """
        black = chess_game.headers["Black"]
        return black

    def user_colour(self, white: str, username: str) -> str:
        """Gets the players colour header from the chess game pgn.

        Args:
            white (str): White players username.
            username (str): Username.

        Returns:
            str: Users colour.
        """
        player = "White" if white == username else "Black"
        return player

    def rating_white(self, chess_game: chess.pgn.Game) -> int:
        """Gets whites rating header from the chess game pgn.

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            int: Whites player rating.
        """
        ratingwhite = int(chess_game.headers["WhiteElo"])
        return ratingwhite

    def rating_black(self, chess_game: chess.pgn.Game) -> int:
        """Gets blacks rating header from the chess game pgn.

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            int: Blacks player rating.
        """
        ratingblack = int(chess_game.headers["BlackElo"])
        return ratingblack

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
        opening_name = str(opening_string.replace("-", " ").strip())
        return opening_name

    def game_termination(self, chess_game: chess.pgn.Game, username) -> str:
        """How the current chess game ended e.g. draw by...

        Args:
            chess_game (chess.pgn.Game): Current chess game.
            username (_type_): Username

        Returns:
            termination (str): How the game ended.
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
        """Gets the users rating.

        Args:
            player (str): A given players username.
            rating_w (int): White rating.
            rating_b (int): Black rating.

        Returns:
           user_rating (int): Players rating.
        """
        user_rating = rating_w if player == "White" else rating_b
        return user_rating

    def rating_opponent(self, player: str, rating_w: int, rating_b: int) -> int:
        """Gets the opponents rating.

        Args:
            player (str): A given players username.
            rating_w (int): White rating.
            rating_b (int): Black rating.

        Returns:
           user_rating (int): Opponents rating.
        """
        opp_rating = rating_b if player == "White" else rating_w
        return opp_rating

    def win_draw_loss(self, chess_game: chess.pgn.Game) -> str:
        """Gets the result of the game (Win/Draw/Loss).

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            str: Win/Draw/Loss
        """
        if chess_game.headers["Result"] == "1-0":
            end_type = "White"
        elif chess_game.headers["Result"] == "0-1":
            end_type = "Black"
        else:
            end_type = "Draw"
        return end_type

    def user_winr(self, winner: str, player: str) -> str:
        """Returns whether the player won/drew/lost the game.

        Args:
            winner (str): _description_
            player (str): Players username.

        Returns:
            str: Win/Draw/Loss
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
        """Date of the game.

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            str: Game date.
        """
        game_date = chess_game.headers["UTCDate"]
        return game_date

    def game_t(self, chess_game: chess.pgn.Game) -> str:
        """Time of the game.

        Args:
            chess_game (chess.pgn.Game): Current chess game.

        Returns:
            str: Game Time.
        """
        game_time = chess_game.headers["UTCTime"]
        return game_time

    def game_dt_time(self, game_date: str, game_time: str) -> datetime:
        """Returns the game datetime of the current chess game.

        Args:
            game_date (str): Game date.
            game_time (str): Game Time.

        Returns:
            datetime: datetime of the current chess game.
        """
        game_date_time = f"{game_date} {game_time}"
        game_datetime = datetime.strptime(game_date_time, "%Y.%m.%d %H:%M:%S")
        return game_datetime

# import chess
# import pandas as pd
import unittest
from src.user_analysis import ChessGameHeaders

# from unittest import mock
# from pandas.testing import assert_frame_equal
# from chess import WHITE
# from chess.engine import PovScore, Cp, Mate
from chess.pgn import read_game
from datetime import datetime


class TestGameHeaders(unittest.TestCase):
    def test_collect_headers(self):
        pass

    def test_time_control(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.time_control(self, chess_game) == "600"

    def test_player_white(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.player_white(self, chess_game) == "JezzaShaw"

    def test_player_black(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.player_black(self, chess_game) == "LucidKoala"

    def test_user_colour_true(self):
        white = "JezzaShaw"
        username = "JezzaShaw"
        assert ChessGameHeaders.user_colour(self, white, username) == "White"

    def test_user_colour_false(self):
        white = "JezzaShaw"
        username = "LucidKoala"
        assert ChessGameHeaders.user_colour(self, white, username) == "Black"

    def test_rating_white(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.rating_white(self, chess_game) == 1011

    def test_test_rating_black(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.rating_black(self, chess_game) == 1009

    def test_opening_cls_no_err(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.opening_cls(self, chess_game) == "A40"

    def test_opening_cls_err(self):
        tempfilepath = BaseFileHandler().test2
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.opening_cls(self, chess_game) == "000"

    def test_opening_nm(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert (
            ChessGameHeaders.opening_nm(self, chess_game)
            == "Queens Pawn Opening Mikenas Defense 2.c4 e5 3.d5"
        )

    def test_game_termination(self):
        tempfilepath = BaseFileHandler().test2
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        username = "LucidKoala"
        assert (
            ChessGameHeaders.game_termination(self, chess_game, username)
            == "Loss by resignation"
        )

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

    def test_win_draw_loss(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.win_draw_loss(self, chess_game) == "White"

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

    def test_game_dt(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.game_dt(self, chess_game) == "2021.02.22"

    def test_game_t(self):
        tempfilepath = BaseFileHandler().test
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert ChessGameHeaders.game_t(self, chess_game) == "19:35:47"

    def test_game_dt_time(self):
        game_date = "2021.02.22"
        game_time = "19:35:47"
        assert ChessGameHeaders.game_dt_time(self, game_date, game_time) == datetime(
            2021, 2, 22, 19, 35, 47
        )


class BaseFileHandler:
    def __init__(self):
        self.test = r"tests/test.pgn"
        self.test2 = r"tests/test2.pgn"

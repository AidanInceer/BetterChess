import datetime
import unittest
from unittest.mock import MagicMock, patch

import pytest
from chess import WHITE
from chess.engine import Cp, Mate, PovScore
from chess.pgn import read_game

from betterchess.core.headers import Headers


class TestGameHeaders(unittest.TestCase):
    def test_time_control(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile.pgn"
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert Headers.time_control(self, chess_game) == "600"

    def test_player_white(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile.pgn"
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert Headers.player_white(self, chess_game) == "JezzaShaw"

    def test_player_black(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile.pgn"
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert Headers.player_black(self, chess_game) == "LucidKoala"

    def test_user_colour_true(self):
        white = "JezzaShaw"
        username = "JezzaShaw"
        assert Headers.user_colour(self, white, username) == "White"

    def test_user_colour_false(self):
        white = "JezzaShaw"
        username = "LucidKoala"
        assert Headers.user_colour(self, white, username) == "Black"

    def test_rating_white(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile.pgn"
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert Headers.rating_white(self, chess_game) == 1011

    def test_test_rating_black(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile.pgn"
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert Headers.rating_black(self, chess_game) == 1009

    def test_opening_cls_no_err(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile.pgn"
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert Headers.opening_cls(self, chess_game) == "A40"

    def test_opening_cls_key_err(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile2.pgn"
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert Headers.opening_cls(self, chess_game) == "000"

    def test_opening_nm(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile.pgn"
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert (
            Headers.opening_nm(self, chess_game)
            == "Queens Pawn Opening Mikenas Defense 2.c4 e5 3.d5"
        )

    def test_opening_nm_keyerror(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile2.pgn"
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert Headers.opening_nm(self, chess_game) == "NA"

    def test_game_termination_loss(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile2.pgn"
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        username = "LucidKoala"
        assert (
            Headers.game_termination(self, chess_game, username)
            == "Loss by resignation"
        )

    def test_game_termination_win(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile2.pgn"
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        username = "JezzaShaw"
        assert (
            Headers.game_termination(self, chess_game, username) == "Win by resignation"
        )

    def test_game_termination_draw(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfiledraw.pgn"
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        username = "LucidKoala"
        assert (
            Headers.game_termination(self, chess_game, username) == "Draw by agreement"
        )

    def test_rating_user(self):
        player = "LucidKoala"
        rating_w = 1011
        rating_b = 1009
        assert Headers.rating_user(self, player, rating_w, rating_b) == 1009

    def test_rating_opponent(self):
        player = "LucidKoala"
        rating_w = 1011
        rating_b = 1009
        assert Headers.rating_opponent(self, player, rating_w, rating_b) == 1011

    def test_win_draw_loss_white(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile.pgn"
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert Headers.win_draw_loss(self, chess_game) == "White"

    def test_win_draw_loss_black(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile2.pgn"
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert Headers.win_draw_loss(self, chess_game) == "Black"

    def test_win_draw_loss_draw(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfiledraw.pgn"
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert Headers.win_draw_loss(self, chess_game) == "Draw"

    def test_user_winr_win(self):
        winner = "White"
        player = "White"
        assert Headers.user_winr(self, winner, player) == "Win"

    def test_user_winr_loss(self):
        winner = "White"
        player = "Black"
        assert Headers.user_winr(self, winner, player) == "Loss"

    def test_user_winr_draw(self):
        winner = "Draw"
        player = "Black"
        assert Headers.user_winr(self, winner, player) == "Draw"

    def test_game_dt(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile.pgn"
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert Headers.game_dt(self, chess_game) == "2021.02.22"

    def test_game_t(self):
        tempfilepath = r"./tests/test_core/fixtures/testpgnfile.pgn"
        chess_game_pgn = open(tempfilepath)
        chess_game = read_game(chess_game_pgn)
        assert Headers.game_t(self, chess_game) == "19:35:47"

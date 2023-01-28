import datetime
import unittest
from unittest.mock import MagicMock, patch

import pytest
from chess import WHITE
from chess.engine import Cp, Mate, PovScore
from chess.pgn import read_game

from betterchess.core.headers import Headers


class TestGameHeaders(unittest.TestCase):
    def setUp(self) -> None:
        self.input_handler = MagicMock()
        self.input_handler.username.return_value = "Ainceer"
        self.file_handler = MagicMock()
        self.run_handler = MagicMock()
        self.run_handler.engine.return_value = "engine"
        self.iter_metadata = MagicMock()
        self.chess_game = MagicMock()
        self.headers = Headers(
            self.input_handler,
            self.file_handler,
            self.run_handler,
            self.iter_metadata,
            self.chess_game,
        )
        self.headers.game_date = "2020"
        self.headers.game_time = "10"
        self.headers.game_datetime = "2020 10"
        self.headers.time_cont = "600"
        self.headers.username = "Ainceer"
        self.headers.player = "white"
        self.headers.user_rating = 1000
        self.headers.opp_rating = 1000
        self.headers.user_winner = True
        self.headers.white = "Ainceer"
        self.headers.black = "Other"
        self.headers.ratingwhite = 1000
        self.headers.ratingblack = 1000
        self.headers.opening_class = "L1"
        self.headers.opening_name = "London"
        self.headers.termination = "win"
        self.headers.end_type = "win"

    @patch(
        "betterchess.core.headers.Headers.create_header_dict",
        return_value={"headers": [1, 2, 3, 4, 5]},
    )
    @patch("betterchess.core.headers.Headers.calculate_headers")
    def test_collect(self, mock_calc, mock_dict):
        output = self.headers.collect()
        mock_calc.assert_called()
        mock_dict.assert_called()
        assert output == {"headers": [1, 2, 3, 4, 5]}

    @patch("betterchess.core.headers.Headers.user_winr")
    @patch("betterchess.core.headers.Headers.rating_opponent")
    @patch("betterchess.core.headers.Headers.rating_user")
    @patch("betterchess.core.headers.Headers.win_draw_loss")
    @patch("betterchess.core.headers.Headers.game_termination")
    @patch("betterchess.core.headers.Headers.opening_nm")
    @patch("betterchess.core.headers.Headers.opening_cls")
    @patch("betterchess.core.headers.Headers.rating_black")
    @patch("betterchess.core.headers.Headers.rating_white")
    @patch("betterchess.core.headers.Headers.user_colour")
    @patch("betterchess.core.headers.Headers.player_black")
    @patch("betterchess.core.headers.Headers.player_white")
    @patch("betterchess.core.headers.Headers.time_control")
    @patch("betterchess.core.headers.Headers.game_dt_time")
    @patch("betterchess.core.headers.Headers.game_t")
    @patch("betterchess.core.headers.Headers.game_dt")
    def test_calculate_headers(
        self,
        m_dt,
        m_t,
        m_dtt,
        m_tc,
        m_pw,
        m_pb,
        m_uc,
        m_rw,
        m_rb,
        m_oc,
        m_on,
        m_gt,
        m_wdl,
        m_ru,
        m_ro,
        m_uw,
    ):
        self.headers.calculate_headers()
        m_dt.assert_called()
        m_t.assert_called()
        m_dtt.assert_called()
        m_tc.assert_called()
        m_pw.assert_called()
        m_pb.assert_called()
        m_uc.assert_called()
        m_rw.assert_called()
        m_rb.assert_called()
        m_oc.assert_called()
        m_on.assert_called()
        m_gt.assert_called()
        m_wdl.assert_called()
        m_ro.assert_called()
        m_uw.assert_called()

    def test_create_header_dict(self):
        expected = {
            "Game_date": "2020",
            "Game_time": "10",
            "Game_datetime": "2020 10",
            "Time_control": "600",
            "Username": "Ainceer",
            "User_Colour": "white",
            "User_rating": 1000,
            "Opponent_rating": 1000,
            "User_winner": True,
            "White_player": "Ainceer",
            "Black_player": "Other",
            "White_rating": 1000,
            "Black_rating": 1000,
            "Opening_class": "L1",
            "Opening_name": "London",
            "Termination": "win",
            "Win_draw_loss": "win",
        }

        output = self.headers.create_header_dict()

        assert expected == output

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

    def test_game_dt_time(self):
        game_date = "2021.02.22"
        game_time = "19:35:47"
        assert self.headers.game_dt_time(game_date, game_time) == datetime.datetime(
            2021, 2, 22, 19, 35, 47
        )

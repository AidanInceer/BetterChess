import unittest
import logging
from src import extract
from datetime import datetime
from unittest.mock import patch
import os


class TestExtract(unittest.TestCase):
    @patch("src.extract.extract_filter")
    def test_data_extract_typeerror(self, mock_ef):
        mock_ef.return_value = 1
        filepath = r"tests/test_files/test_pgn2.csv"
        logfilepath = r"tests/test_files/test_extract.log"
        open(logfilepath, "x")
        open(filepath, "x")
        username = "JM333"
        logging.basicConfig(
            filename=logfilepath,
            format="[%(levelname)s %(module)s] %(message)s",
            level=logging.INFO,
            datefmt="%Y/%m/%d %I:%M:%S",
        )
        logger = logging.getLogger(__name__)
        self.assertRaises(
            TypeError, extract.data_extract(username, filepath, logfilepath, logger)
        )
        os.remove(filepath)
        os.remove(logfilepath)

    def test_data_extract(self):
        filepath = r"tests/test_files/test_pgn2.csv"
        logfilepath = r"tests/test_files/test_extract.log"
        open(logfilepath, "x")
        open(filepath, "x")
        username = "JM333"
        logging.basicConfig(
            filename=logfilepath,
            format="[%(levelname)s %(module)s] %(message)s",
            level=logging.INFO,
            datefmt="%Y/%m/%d %I:%M:%S",
        )
        logger = logging.getLogger(__name__)
        assert extract.data_extract(username, filepath, logfilepath, logger) is None
        os.remove(filepath)
        os.remove(logfilepath)

    @patch("src.extract.collect_game_data")
    def test_extract_filter_cgd(self, mock_cgd):
        mock_cgd.return_value = 1
        url = "https://api.chess.com/pub/player/EZE-123/games/2021/11"
        in_log = False
        in_curr = True
        filepath = r"tests/test_files/test_pgn.csv"
        logfilepath = r"tests/test_files/test.log"
        assert extract.extract_filter(in_log, in_curr, url, filepath, logfilepath) == 1

    @patch("src.extract.filter_pgncsv")
    def test_extract_filter_fp(self, mock_fp):
        mock_fp.return_value = 1
        url = "https://api.chess.com/pub/player/EZE-123/games/2021/11"
        in_log = True
        in_curr = True
        filepath = r"tests/test_files/test_pgn.csv"
        logfilepath = r"tests/test_files/test.log"
        assert extract.extract_filter(in_log, in_curr, url, filepath, logfilepath) == []

    def test_extract_filter(self):
        url = "https://api.chess.com/pub/player/EZE-123/games/2021/11"
        in_log = True
        in_curr = False
        filepath = r"tests/test_files/test_pgn.csv"
        logfilepath = r"tests/test_files/test.log"
        assert extract.extract_filter(in_log, in_curr, url, filepath, logfilepath) == []

    def test_filter_pgncsv(self):
        filepath = r"tests/test_files/test_pgn.csv"
        logfilepath = r"tests/test_files/test.log"
        assert extract.filter_pgncsv(filepath, logfilepath) is None

    def test_collect_game_data(self):
        url = "https://api.chess.com/pub/player/EZE-123/games/2021/11"
        assert extract.collect_game_data(url) == extract.collect_game_data(url)

    def test_collect_game_data_type(self):
        url = "https://api.chess.com/pub/player/EZE-123/games/2021/11"
        assert type(extract.collect_game_data(url)) is list

    def test_url_in_log_false(self):
        url = "https://api.chess.com/pub/player/ainceer/games/2021/11"
        logfilepath = r"tests/test_files/test.log"
        assert extract.url_in_log(url, logfilepath) is False

    def test_url_in_log_true(self):
        url = "https://api.chess.com/pub/player/ainceer/games/2021/01"
        logfilepath = r"tests/test_files/test.log"
        assert extract.url_in_log(url, logfilepath) is True

    def test_in_cur_mth_false(self):
        url = "https://api.chess.com/pub/player/ainceer/games/2021/11"
        assert extract.in_curr_month(url) is False

    @patch("src.extract.get_url_date")
    @patch("src.extract.get_curr_mth")
    def test_in_cur_mth_true(self, mock_gud, mock_gcm):
        url = "https://api.chess.com/pub/player/ainceer/games/2021/11"
        mock_gud.return_value = "2021-11-01"
        mock_gcm.return_value = "2021-11-01"
        assert extract.in_curr_month(url) is True

    def test_get_curr_month(self):
        curmth = datetime.strptime("2022-07-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        assert curmth == extract.get_curr_mth()

    def test_get_url_date(self):
        url = "https://api.chess.com/pub/player/ainceer/games/2020/11"
        url_date = datetime.strptime("2020-11-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        assert url_date == extract.get_url_date(url)

    def test_simple_progress_bar_t0(self):
        test_type = 0
        num = 1
        total = 100
        assert extract.simple_progress_bar(num, total, test_type) is None

    def test_simple_progress_bar_t1(self):
        test_type = 1
        num = 1
        total = 100
        assert extract.simple_progress_bar(num, total, test_type) is None
